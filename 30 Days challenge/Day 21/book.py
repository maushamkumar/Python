import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urljoin, urlparse
import os

class BooksScraper:
    def __init__(self, base_url="http://books.toscrape.com/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.books_data = []

    def get_page(self, url):
        """Fetch a webpage with error handling"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_rating(self, rating_class):
        """Convert rating class to number"""
        rating_map = {
            'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
        }
        for word in rating_class:
            if word in rating_map:
                return rating_map[word]
        return 0

    def clean_price(self, price_text):
        """Extract numeric price from price string"""
        if price_text:
            # Remove currency symbols and extract numbers
            price = re.sub(r'[^\d.]', '', price_text)
            try:
                return float(price)
            except ValueError:
                return 0.0
        return 0.0

    def scrape_book_details(self, book_url):
        """Scrape detailed information from individual book page"""
        response = self.get_page(book_url)
        if not response:
            return {}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        details = {}
        
        try:
            # Get description
            product_description = soup.find('div', {'id': 'product_description'})
            if product_description:
                description_p = product_description.find_next_sibling('p')
                details['description'] = description_p.text.strip() if description_p else "No description available"
            else:
                details['description'] = "No description available"
            
            # Get product information table
            table = soup.find('table', class_='table table-striped')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    th = row.find('th')
                    td = row.find('td')
                    if th and td:
                        key = th.text.strip()
                        value = td.text.strip()
                        details[key.lower().replace(' ', '_')] = value
            
        except Exception as e:
            print(f"Error parsing book details from {book_url}: {e}")
        
        return details

    def scrape_books_from_page(self, page_url):
        """Scrape all books from a single page"""
        print(f"Scraping page: {page_url}")
        response = self.get_page(page_url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        books = []
        
        # Find all book containers
        book_containers = soup.find_all('article', class_='product_pod')
        
        for container in book_containers:
            try:
                book_data = {}
                
                # Book title
                title_element = container.find('h3').find('a')
                book_data['title'] = title_element.get('title', '').strip()
                
                # Book URL
                book_relative_url = title_element.get('href', '')
                book_data['book_url'] = urljoin(self.base_url, book_relative_url)
                
                # Book image URL
                img_element = container.find('div', class_='image_container').find('img')
                img_relative_url = img_element.get('src', '')
                book_data['image_url'] = urljoin(self.base_url, img_relative_url)
                
                # Price
                price_element = container.find('p', class_='price_color')
                book_data['price'] = price_element.text.strip() if price_element else "N/A"
                book_data['price_numeric'] = self.clean_price(book_data['price'])
                
                # Rating
                rating_element = container.find('p', class_='star-rating')
                if rating_element:
                    rating_classes = rating_element.get('class', [])
                    book_data['rating'] = self.parse_rating(rating_classes)
                else:
                    book_data['rating'] = 0
                
                # Availability
                availability_element = container.find('p', class_='instock availability')
                book_data['availability'] = availability_element.text.strip() if availability_element else "Unknown"
                
                # Get detailed information from book's individual page
                print(f"  Scraping details for: {book_data['title']}")
                book_details = self.scrape_book_details(book_data['book_url'])
                book_data.update(book_details)
                
                books.append(book_data)
                
                # Add small delay to be respectful
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error processing book container: {e}")
                continue
        
        return books

    def get_all_page_urls(self):
        """Get URLs for all pages"""
        page_urls = []
        current_url = self.base_url
        
        while current_url:
            page_urls.append(current_url)
            
            # Get the current page to find next page link
            response = self.get_page(current_url)
            if not response:
                break
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find next page link
            next_link = soup.find('li', class_='next')
            if next_link:
                next_relative_url = next_link.find('a').get('href')
                current_url = urljoin(current_url, next_relative_url)
            else:
                current_url = None
        
        return page_urls

    def scrape_all_books(self, max_pages=None):
        """Scrape all books from all pages"""
        print("Starting to scrape Books to Scrape website...")
        
        # Get all page URLs
        page_urls = self.get_all_page_urls()
        
        if max_pages:
            page_urls = page_urls[:max_pages]
        
        print(f"Found {len(page_urls)} pages to scrape")
        
        # Scrape books from each page
        for i, page_url in enumerate(page_urls, 1):
            print(f"\n--- Page {i}/{len(page_urls)} ---")
            books = self.scrape_books_from_page(page_url)
            self.books_data.extend(books)
            print(f"Scraped {len(books)} books from page {i}")
            
            # Add delay between pages
            time.sleep(1)
        
        print(f"\nTotal books scraped: {len(self.books_data)}")
        return self.books_data

    def save_to_csv(self, filename="books_data.csv"):
        """Save scraped data to CSV using pandas"""
        if not self.books_data:
            print("No data to save!")
            return
        
        # Create DataFrame
        df = pd.DataFrame(self.books_data)
        
        # Reorder columns for better readability
        desired_columns = [
            'title', 'price', 'price_numeric', 'rating', 'availability', 
            'description', 'book_url', 'image_url', 'upc', 'product_type',
            'price_(excl._tax)', 'price_(incl._tax)', 'tax', 'number_of_reviews'
        ]
        
        # Only include columns that exist in the data
        existing_columns = [col for col in desired_columns if col in df.columns]
        remaining_columns = [col for col in df.columns if col not in existing_columns]
        final_columns = existing_columns + remaining_columns
        
        df = df[final_columns]
        
        # Save to CSV
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Data saved to {filename}")
        
        # Display basic statistics
        print(f"\nDataset Statistics:")
        print(f"Total books: {len(df)}")
        print(f"Average price: £{df['price_numeric'].mean():.2f}")
        print(f"Price range: £{df['price_numeric'].min():.2f} - £{df['price_numeric'].max():.2f}")
        print(f"Average rating: {df['rating'].mean():.1f}/5")
        
        return df

    def display_sample_data(self, n=5):
        """Display sample of scraped data"""
        if not self.books_data:
            print("No data available!")
            return
        
        df = pd.DataFrame(self.books_data)
        print(f"\nSample of scraped data (first {n} books):")
        print("=" * 80)
        
        for i in range(min(n, len(df))):
            book = df.iloc[i]
            print(f"Book {i+1}:")
            print(f"  Title: {book['title']}")
            print(f"  Price: {book['price']}")
            print(f"  Rating: {book['rating']}/5")
            print(f"  Availability: {book['availability']}")
            print(f"  Description: {book['description'][:100]}..." if len(book['description']) > 100 else f"  Description: {book['description']}")
            print("-" * 40)

def main():
    """Main function to run the scraper"""
    scraper = BooksScraper()
    
    # You can limit the number of pages for testing
    # scraper.scrape_all_books(max_pages=2)  # Scrape only first 2 pages
    
    # Scrape all books (this will take some time - around 1000 books across 50 pages)
    books_data = scraper.scrape_all_books()
    
    if books_data:
        # Display sample data
        scraper.display_sample_data()
        
        # Save to CSV
        df = scraper.save_to_csv("books_to_scrape_data.csv")
        
        print("\nScraping completed successfully!")
        print(f"CSV file 'books_to_scrape_data.csv' has been created with {len(books_data)} books.")
    else:
        print("No data was scraped!")

if __name__ == "__main__":
    # Install required packages if not already installed
    # pip install requests beautifulsoup4 pandas lxml
    
    main()