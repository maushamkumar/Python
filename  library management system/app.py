import os 
import json 
import datetime 
import getpass 
from typing import Dict, List, Optional

class Book: 
    def __init__(self, book_id:int, name:str, author:str, copies:int, price:float):
        self.id = book_id
        self.name = name
        self.author = author
        self.copies = copies
        self.copies_left = copies
        self.price = price
        
    def to_dict(self):
        return{
            'id': self.id, 
            'name': self.name, 
            'author': self.author, 
            'copies': self.copies, 
            'copies_left': self.copies_left, 
            'price': self.price
            
        }
    @classmethod
    def from_dict(cls, data):
        book = cls(data['id'], data['name'], data['author'], data['copies'], data['price'])
        book.copies_left = data['copies_left']
        return book
    
class User:
    def __init__(self, user_id:int, name:str):
        self.id = user_id
        self.name = name 
        self.book_id = 0 
        self.issue_date = None
        self.due_date = None
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'book_id': self.book_id,
            'issue_date': self.issue_date.strftime("%d-%m-%Y %H:%M:%S") if self.issue_date else None,
            'due_date': self.due_date.strftime("%d-%m-%Y %H:%M:%S") if self.due_date else None
        }

        
    @classmethod
    def from_dict(cls, data):
        user = cls(data['id'], data['name'])
        user.book_id = data.get('book_id', 0)
        user.issue_date = datetime.datetime.strptime(data['issue_date'], "%d-%m-%Y %H:%M:%S") if data.get('issue_date') else None
        user.due_date = datetime.datetime.strptime(data['due_date'], "%d-%m-%Y %H:%M:%S") if data.get('due_date') else None
        return user

    

class LibraryManager:
    def __init__(self):
        self.book_file = 'book.json'
        self.users_file = 'user.json'
        self.admin_password = 'library'
        self.main_password = 'libpass'
        self.books: Dict[int, Book] = {}
        self.users: Dict[int, User] = {}
        self.load_data()
        
    def load_data(self):
        """Load books and users from JSON file """
        try: 
            if os.path.exists(self.book_file):
                with open(self.book_file, 'r') as f:
                    books_data = json.load(f)
                    self.books = {int(k): Book.from_dict(v) for k, v in books_data.items()}
        except Exception as e:
            print(f"Error Loading books: {e}")
            
        try: 
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    users_data = json.load(f)
                    self.users = {int(k): User.from_dict(v) for k, v in users_data.items()}
        except Exception as e:
            print(f"Error Loading users: {e}")
            
    def save_books(self):
        """Save books to JSON file"""
        try: 
            books_data = {str(k): v.to_dict() for k, v in self.books.items()}
            with open(self.book_file, 'w') as f:
                json.dump(books_data, f, indent=2)
        except Exception as e:
            print(f"Error saving Books: {e}")
            
    def save_users(self):
        """Save users to JSON file"""
        try:
            users_data = {str(k): v.to_dict() for k, v in self.users.items()}
            with open(self.users_file, 'w') as f:
                json.dump(users_data, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
            
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self, title:str):
        """Display header with title"""
        self.clear_screen()
        print('-' * 80)
        print(f"{title:^80}")
        print('-' * 80)
        print(f"Current Time: {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}")
        print('-' * 80)
        
    def authenticate(self, password: str, attempts: int = 3)-> bool:
        """Authenticate User with Passwrod"""
        for attempt in range(attempts):
            self.clear_screen()
            print(f"Authentication Required - Attempts left: {attempts - attempt}")
            entered_password = getpass.getpass("Enter password:")
            
            if entered_password == password:
                print("Authentication Successful!")
                input("Press enter to continue..")
                return True
            else:
                print("Invalid Password")
                if attempt < attempts - 1:
                    input("Press Enter to try again...")
        print("Authentication failed Exiting...")
        return False
    

    def main_menu(self):
        """Main menu of the application"""
        if not self.authenticate(self.main_password):
            return
        
        while True:
            self.display_header("LIBRARY MANAGEMENT SYSTEM - MAIN MENU")
            print("1. Administrator")
            print('2. User')
            print('3. Exit')
            
            try:
                choice = int(input("\nEnter your choice: "))
                
                if choice == 1:
                    self.admin_menu()
                elif choice == 2:
                    self.user_menu()
                elif choice == 3: 
                    if self.confirm_exit():
                        break
                else:
                    print("Invalid Choice")
                    input("Press Enter to Continue...")
            except ValueError:
                print("Please enter a valid number!")
                input("Press Enter to continue...")
    
    def admin_menu(self):
        """Administrator Menu"""
        if not self.authenticate(self.admin_password):
            return
        
        while True:
            self.display_header("ADMINISTRATOR MENU")
            print("1. Add/Edit Book")
            print("2. Add/Edit User")
            print("3. List Books")
            print("4. List Users")
            print("5. Issue Book")
            print("6. Collect Book")
            print("7. Main Menu")
            print("8. Exit")
            
            
            try:
                choice = int(input("\nEnter your choice: "))
                if choice == 1: 
                    self.book_menu()
                elif choice == 2: 
                    self.user_management_menu()
                elif choice == 3: 
                    self.list_book()
                elif choice == 4: 
                    self.list_users()
                elif choice == 5:
                    self.issue_book()
                elif choice == 6:
                    self.collect_book
                elif choice == 7: 
                    self.main_menu()
                elif choice == 8: 
                    if self.confirm_exit():
                        break
                else:
                    print("Invalid Choice")
                    input("Press Enter to Continue...")
            except ValueError:
                print("Please enter a valid number!")
                input("Press Enter to continue...")
                
    def book_menu(self):
        """Book Managment menu"""
        while True:
            self.display_header("BOOK MENU")
            print('1. Add Book')
            print("2. Edit Book Details")
            print("3. Delete Book")
            print("4. Administrator menu")
            print("5. Exit")
            
            try: 
                choice = int(input("\nEnter your choice"))
                
                if choice == 1: 
                    self.add_book()
                elif choice == 2:
                    self.edit_book()
                elif choice == 3: 
                    self.delete_book()
                elif choice == 4: 
                    return
                elif choice == 5: 
                    if self.confirm_exit():
                        break
                else:
                    print("Invalid Choice")
                    input("Press Enter to Continue...")
            except Exception as e:
                print("Please enter a valid number!")
                input("Press Enter to continue...")
            
            
    def add_book(self):
        """Add a new book"""
        while True:
            self.display_header("ADD BOOK")
            
            try:
                book_id = int(input("Enter BOOK ID:"))
                
                if book_id in self.books:
                    print("Book ID already exists!")
                    input("Press Enter to continue...")
                    continue
                name = input("Enter Book Name: ").strip()
                author = input("Enter Author Name: ").strip()
                copies = int(input("Enter Number of Copies: "))
                price = float(input("Enter Price: "))
                
                book = Book(book_id, name, author, copies, price)
                self.books[book_id] = book
                self.save_books()
                
                print("Book successfully added!")
                if input("Do you want to add another book? (y/n): ").lower() != 'y':
                    break
            except ValueError:
                print("Please enter valid values!")
                input("Press Enter to continue...")
                
    def edit_book(self):
        """Edit book details"""
        self.display_header("EDIT BOOK DETAILS")
        try:
            book_id = int(input("Enter Book ID to edit:"))
            
            if book_id not in self.books:
                print("Book ID does not exist!")
                input("Press Enter to continue... ")
                return
            book = self.books[book_id]
            while True:
                self.display_header("EDIT BOOK DETAILS")
                print(f"Current Book Information:")
                print(f"Book ID: {book_id}")
                print(f"1. Book Name: {book.name}")
                print(f"2. Author: {book.author}")
                print(f"3. Number of copies {book.copies}")
                print(f"4. Price: {book.price:.2f}")
                
                field_choice = int(input("\nEnter the field to edit: "))
                if field_choice == 1:
                    book.name = input("Enter new book name: ").strip()
                elif field_choice == 2: 
                    book.author = input("Enter Author Name: ").strip()
                elif field_choice == 3:
                    book.copies = int(input("Enter Number of Copies: "))
                elif field_choice == 4:
                    book.price = float(input("Enter Price: "))
                else:
                    print("Invalid choice!")
                    continue
                if input("Do you want to edit anything else? (y/n): ").lower() != 'y':
                    break
            self.save_books()
            print("Book successfully update")
            input("Press Enter to continue...")
            
        except ValueError:
            print("Please enter valid values!")
            input("Press enter to continue...")
            
    def delete_book(self):
        """Delete a book"""
        self.display_header("DELETE BOOK")

        try:
            book_id = int(input("Enter Book ID to delete: "))
            
            if book_id not in self.books:
                print("Book ID does not exist!")
                input("Press enter to continue")
                return
            del self.books[book_id]
            self.save_books()
            print("Book successfully deleted")
            input("Press enter to continue...")
        except ValueError: 
            print("Please enter a valid Book ID")
            input("press Enter to continue...")
        
    def user_management_menu(self):
        """User Management menu"""
        while True:
            self.display_header("USER MENU")
            print("1. Add User")
            print("2. Edit User Details")
            print("3. Delete User")
            print("4. Adminstrator Menu")
            print("5. Exit")
            
            try:
                choice = int(input("\nEnter you choice: "))
                
                if choice == 1:
                    self.add_user()
                elif choice == 2: 
                    self.edit_user()
                elif choice == 3:
                    self.delete_user()
                elif choice == 4:
                    return
                elif choice == 5:
                    if self.onfirm_exit():
                        exit()
                else:
                    print("Invalid choice!")
                    input("Press Enter to continue...")
            except ValueError:
                print("Please enter a valid number!")
                input("Press Enter to continue...")
                
    def add_user(self):
        """Add a new user"""
        while True:
            self.display_header("ADD USER")
            
            try:
                user_id = int(input("Enter User ID: "))
                
                if user_id in self.users:
                    print("User ID already exists!")
                    input("Press Enter to continue...")
                    continue
                
                name = input("Enter Name: ").strip()
                
                user = User(user_id, name)
                self.users[user_id] = user
                self.save_users()
                
                print("User successfully added!")
                
                if input("Do you want to add another user? (y/n): ").lower() != 'y':
                    break
                    
            except ValueError:
                print("Please enter valid values!")
                input("Press Enter to continue...")
                
    def edit_user(self):
        """Edit user details"""
        self.display_header("EDIT USER DETAILS")
        
        try:
            user_id = int(input("Enter User ID to edit: "))
            
            if user_id not in self.users:
                print("User ID does not exist!")
                input("Press Enter to continue...")
                return
            
            user = self.users[user_id]
            
            while True:
                self.display_header("EDIT USER DETAILS")
                print(f"Current User Information")
                print(f"1. User ID: {user.id}")
                print(f"2. User Name: {user.name}")
                
                field_choice = int(input("Enter new user ID"))
                if field_choice == 1: 
                    new_id = int(input("Enter new user ID: "))
                    if new_id in self.users and new_id != user_id:
                        print("User ID already exists!")
                        continue
                    
                    del self.users[user_id]
                    user.id = new_id
                    self.users[new_id] = user
                    user_id = new_id
                elif field_choice == 2:
                    user.name = input("Enter new user name: ").strip()
                else:
                    print("Invalid choice")
                    
                if input("Do you want to edit anything esle? (y/n): ").lower() != 'y':
                    break
            self.save_users()
            print("User successfully updated")
            input("press Enter to continue...")
        except ValueError:
            print("Please Enter valid values")
            input("Press Enter to continue...")
            
    def delete_user(self):
        """Delete a User """
        self.display_header("DELETE USER")
        try:
            user_id = int(input("Enter User Id to delete: "))
            
            if user_id not in self.users:
                print("User Id does not exist")
                input("Press Enter to continue...")
                return
            del self.users[user_id]
            self.save_users()
            print("User successfully deleted!")
            input("Press Enter to continue... ")
            
        except ValueError:
            print("Please Enter valid values")
            input("Press Enter to continue...")
            
    def list_book(self):
        """List all the books"""
        self.display_header("LIST RECORD")
        
        if not self.books:
            print("No book found")
        else:
            print(f"{'ID': <5} {'Book Name':<25} {'Author': <20} {'Price':<8}{"Copies":<8} {'Left':<8}")
            print("-" * 80)
            for book in self.books.values():
                print(f"{book.id: <5} {book.name: <25} {book.author: <20} {book.price: <8.2f} {book.copies:<8} {book.copies_left:<8}")
                
        input("\nPress Enter to continue...")
        
    def list_user(self):
        """Display all users"""
        self.display_header("USER RECORD")
        
        if not self.users:
            print("No users found!")
        else:
            print(f"{'ID':<5} {'Name':<20} {'Book ID':<8} {'Issue Date':<12} {'Due Date':<12}")
            print("-" * 80)
            for user in self.users.values():
                issue_date = user.issue_date.strftime("%d-%m-%Y") if user.issue_date else "None"
                due_date = user.due_date.strftime("%d-%m-%Y") if user.due_date else "None"
                print(f"{user.id:<5} {user.name:<20} {user.book_id:<8} {issue_date:<12} {due_date:<12}")
        input("\nPress Enter to continue...")
        
    def issue_book(self):
        """Issue a book to a user"""
        self.display_header("ISSUE BOOK")
        
        try:
            user_id = int(input("Enter User ID: "))
            
            if user_id not in self.users:
                print("User ID does not exist!")
                input("Press Enter to continue...")
                return
            
            user = self.users[user_id]
            
            if user.book_id > 0:
                print("User has already been issued a book!")
                input("Press Enter to continue...")
                return
            
            book_id = int(input("Enter Book ID to issue: "))
            if book_id not in self.books:
                print("Book ID does not exist!")
            
            book = self.books[book_id]
            
            if book.copies_left == 0:
                print("Book is not available!")
                input("Press Enter to continue...")
                return
            
            # Issue the book 
            issue_date = datetime.datetime.now()
            due_date = issue_date + datetime.timedelta(days=15)
            
            user.book_id = book_id
            user.issue_date = issue_date
            user.due_date = due_date
            
            book.copies_left -= 1
            
            print(f"Book issued successfully!")
            print(f"Issue Date: {issue_date.strftime('%d-%m-%Y')}")
            print(f"Due Date: {due_date.strftime('%d-%m-%Y')}")
            input("Press Enter to continue...")
        except ValueError:
            print("Please enter valid values!")
            input("Press Enter to continue...")
            
    def collect_book(self):
        """Collect a book from a user"""
        self.display_header("COLLECT BOOK")
        
        try:
            user_id = int(input("Enter User ID: "))
            
            if user_id not in self.users:
                print("User ID does not exist!")
                input("Press Enter to continue...")
                return
            
            user = self.users[user_id]
            
            if user.book_id == 0:
                print("No book issued to this user!")
                input("Press Enter to continue...")
                return
            
            return_date = datetime.datetime.now()
            
            # Calculate fine 
            fine_amount = 0 
            if return_date > user.due_date:
                days_late = (return_date - user.due_date).days
                fine_amount = days_late * 3
                
                
            # Return the book 
            book = self.books[user.book_id]
            book.copies_left += 1
            
            user.book_id = 0 
            user.issue_date = None
            user.due_date = None
            
            self.save_users()
            self.save_books()
            
            print("Book returned successfully!")
            if fine_amount > 0 :
                print(f"Fine amount: ${fine_amount}")
            input("Press Enter to continue...")
            
        except ValueError:
            print("Please enter a valid User ID!")
            input("Press Enter to continue...")
            
            
    def user_menu(self):
        """User Menu"""
        while True:
            self.display_header("USER MENU")
            print("1. Search Book")
            print("2. User Info")
            print("3. Main Menu")
            print("4. Exit")
            
            try:
                choice = int(input("\nEnter your choice: "))
                
                if choice == 1:
                    self.search_book()
                elif choice == 2: 
                    self.user_info()
                elif choice == 3:
                    return
                elif choice == 4:
                    if self.confirm_exit():
                        exit()
                        
            except ValueError:
                print("Please enter a valid Number!")
                input("Press Enter to continue...")
                
    def search_book(self):
        """Search for books"""
        while True:
            self.display_header("BOOK SEARCH")
            
            search_name = input("Enter the name of the book to search: ").strip().lower()
            found_books = []
            
            for book in self.books.values():
                if search_name in book.name.lower():
                    found_books.append(book)
                    
            if found_books:
                print(f"\nSearch Results: {len(found_books)} book(s) found")
                print("-" * 80)
                for i, book in enumerate(found_books, 1):
                    print(f"\nResult {i}:")
                    print(f"Book ID: {book.id}")
                    print(f"Book Name: {book.name}")
                    print(f"Author: {book.author}")
                    print(f"Price: ${book.price:.2f}")
                    print(f"Copies Available: {book.copies_left}")
            else:
                print("No such book found!")
            
            if input("\nDo you want to search for another book? (y/n): ").lower() != 'y':
                break
            
    def user_info(self):
        """Display user Information"""
        while True:
            self.display_header("USER INFORMATION")
            
            try:
                user_id = int(input("Enter User ID: "))
                
                if user_id not in self.users:
                    print("User ID does not exist!")
                    input("Press Enter to continue...")
                    return
                
                if user_id in self.users:
                    user = self.users[user_id]
                    print("\nUser Information:")
                    print(f"user ID: {user.id}")
                    print(f"Name: {user.name}")
                    print(f"Book ID: {user.book_id}")
                    
                    if user.issue_date:
                        print(f"Issue Date: {user.issue_date.strftime('%d-%m-%Y')}")
                        print(f"Due Date: {user.due_date.strftime('%d-%m-%Y')}")
                        
                    else:
                        print("No book currently issued")
                else:
                    print("No such user found!")
                    
                if input("\nDo you want to search for another book? (y/n): ").lower() != 'y':
                    break
                
            except ValueError:
                print("Please enter a valid User ID!")
                input("Press Enter to continue...")
                
    def confirm_exit(self):
        """Confirm exit"""
        return input("Do you want to exit? (y/n): ").lower() == 'y'
    
def main():
    """Main function"""
    library = LibraryManager()
    print("Welcome to Library Managment System")
    print("Press Enter to continue...")
    
    try:
        library.main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting program....")
        
    print("Thank you for using Library Management System!")
    
if __name__ == "__main__":
    main()