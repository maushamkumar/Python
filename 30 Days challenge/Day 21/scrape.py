import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
import pandas as pd

class CricketScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def scrape_cricbuzz_live(self, team1="india", team2="australia"):
        """Scrape live matches from Cricbuzz - Enhanced version"""
        st.write(f"🔍 Checking Cricbuzz for {team1} vs {team2} matches...")
        url = "https://www.cricbuzz.com/cricket-match/live-scores"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            matches = []
            # Multiple selectors to find match cards
            selectors = [
                'div.cb-mtch-lst',
                'div[class*="match"]',
                'div.cb-schdl',
                'div.cb-col-100'
            ]
            
            for selector in selectors:
                match_cards = soup.select(selector)
                if match_cards:
                    st.write(f"Found {len(match_cards)} cards with selector: {selector}")
                    break
            
            for card in match_cards:
                try:
                    card_text = card.get_text().lower()
                    
                    # Check for team combinations
                    team_combinations = [
                        (team1.lower(), team2.lower()),
                        ('ind', 'aus'),
                        ('india', 'australia'),
                        ('eng', 'ind'),
                        ('england', 'india')
                    ]
                    
                    match_found = False
                    for t1, t2 in team_combinations:
                        if (t1 in card_text and t2 in card_text):
                            match_found = True
                            break
                    
                    if match_found:
                        # Extract more detailed information
                        teams_info = card.find_all('div', class_='cb-ovr-flo')
                        match_link = card.find('a')
                        
                        # Try to get score information
                        score_divs = card.find_all('div', class_=re.compile(r'scr|score'))
                        status_divs = card.find_all('div', class_=re.compile(r'status|state'))
                        
                        match_info = {
                            'source': 'Cricbuzz',
                            'teams': ' '.join([team.get_text().strip() for team in teams_info]) if teams_info else card_text[:100],
                            'url': 'https://www.cricbuzz.com' + match_link.get('href') if match_link else None,
                            'scores': ' | '.join([score.get_text().strip() for score in score_divs]) if score_divs else 'Score not available',
                            'status': ' '.join([status.get_text().strip() for status in status_divs]) if status_divs else 'Status unknown',
                            'full_text': card_text[:200] + '...' if len(card_text) > 200 else card_text
                        }
                        
                        matches.append(match_info)
                        
                except Exception as e:
                    continue
            
            return matches
            
        except Exception as e:
            st.error(f"❌ Error scraping Cricbuzz: {e}")
            return []
    
    def scrape_espn_live(self, team1="india", team2="australia"):
        """Scrape live matches from ESPNCricinfo - Enhanced version"""
        st.write(f"🔍 Checking ESPNCricinfo for {team1} vs {team2} matches...")
        url = "https://www.espncricinfo.com/live-cricket-score"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            matches = []
            # Multiple selectors to try
            selectors = [
                'div[data-testid="match-card"]',
                '.ds-rounded-lg',
                '.match-block',
                'div.ds-p-4',
                'div[class*="match"]',
                'div[class*="card"]'
            ]
            
            for selector in selectors:
                cards = soup.select(selector)
                if cards:
                    st.write(f"Found {len(cards)} cards with selector: {selector}")
                    
                    for card in cards:
                        text = card.get_text().lower()
                        
                        # Check for team combinations
                        team_combinations = [
                            (team1.lower(), team2.lower()),
                            ('ind', 'aus'),
                            ('india', 'australia'),
                            ('eng', 'ind'),
                            ('england', 'india')
                        ]
                        
                        match_found = False
                        for t1, t2 in team_combinations:
                            if (t1 in text and t2 in text):
                                match_found = True
                                break
                        
                        if match_found:
                            link = card.find('a')
                            
                            # Try to extract scores and status
                            score_elements = card.find_all(text=re.compile(r'\d+/\d+|\d+ runs'))
                            status_elements = card.find_all(text=re.compile(r'live|finished|upcoming'))
                            
                            matches.append({
                                'source': 'ESPNCricinfo',
                                'teams': card.get_text()[:150] + '...' if len(card.get_text()) > 150 else card.get_text(),
                                'url': 'https://www.espncricinfo.com' + link.get('href') if link else None,
                                'scores': ' | '.join(score_elements) if score_elements else 'Score not available',
                                'status': ' | '.join(status_elements) if status_elements else 'Status unknown',
                                'full_text': text[:200] + '...' if len(text) > 200 else text
                            })
                    break
            
            return matches
            
        except Exception as e:
            st.error(f"❌ Error scraping ESPNCricinfo: {e}")
            return []
    
    def scrape_any_cricket_data(self):
        """Get any available cricket data for demonstration - Enhanced version"""
        st.write("🔍 Getting general cricket data...")
        
        urls_to_try = [
            "https://www.espncricinfo.com/scores",
            "https://www.cricbuzz.com/cricket-match/live-scores",
            "https://www.espncricinfo.com/cricket-match"
        ]
        
        all_data = []
        
        for url in urls_to_try:
            try:
                st.write(f"Trying: {url}")
                response = requests.get(url, headers=self.headers, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                matches = []
                
                # 1. Look for links with cricket content
                links = soup.find_all('a', href=True)
                for link in links[:30]:  # Increased from 20 to 30
                    href = link.get('href', '')
                    text = link.get_text().strip()
                    
                    if text and len(text) > 10:
                        cricket_keywords = ['vs', 'v ', 'match', 'india', 'australia', 'england', 'cricket', 'runs', 'wickets', 'overs']
                        if any(keyword in text.lower() for keyword in cricket_keywords):
                            matches.append({
                                'text': text[:100] + '...' if len(text) > 100 else text,
                                'url': href if href.startswith('http') else url + href,
                                'type': 'Link'
                            })
                
                # 2. Look for div elements with match content
                divs = soup.find_all('div')
                for div in divs[:50]:  # Increased from 30 to 50
                    text = div.get_text().strip()
                    if text and 20 < len(text) < 200:
                        cricket_keywords = ['vs', 'v ', 'won by', 'lost by', 'runs', 'wickets', 'ind', 'aus', 'eng']
                        if any(keyword in text.lower() for keyword in cricket_keywords):
                            matches.append({
                                'text': text,
                                'source': url,
                                'type': 'Match Info'
                            })
                
                # 3. Look for specific score patterns
                score_pattern = re.compile(r'\d+/\d+|\d+\s*runs|\d+\s*wickets', re.I)
                score_elements = soup.find_all(text=score_pattern)
                for score in score_elements[:10]:
                    parent = score.parent
                    if parent:
                        context = parent.get_text().strip()
                        if len(context) > 20:
                            matches.append({
                                'text': context[:100] + '...' if len(context) > 100 else context,
                                'source': url,
                                'type': 'Score'
                            })
                
                if matches:
                    all_data.extend(matches[:10])  # Top 10 from each source
                    break  # If we found data, stop trying other URLs
                    
            except Exception as e:
                st.write(f"❌ Error with {url}: {e}")
                continue
        
        return all_data
    
    def debug_page_structure(self, url):
        """Debug what's actually on the page - Enhanced version"""
        st.write(f"🔧 Debugging page structure for: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            debug_info = {
                'status_code': response.status_code,
                'title': soup.title.text if soup.title else 'No title',
                'match_divs': len(soup.find_all('div', class_=re.compile(r'match', re.I))),
                'all_divs_count': len(soup.find_all('div')),
                'cricket_terms': []
            }
            
            # Look for cricket terms
            cricket_terms = ['india', 'australia', 'england', 'runs', 'wickets', 'overs', 'innings', 'live', 'score']
            page_text = soup.get_text().lower()
            
            found_terms = [term for term in cricket_terms if term in page_text]
            debug_info['cricket_terms'] = found_terms
            
            return debug_info
            
        except Exception as e:
            return {'error': str(e)}

# Streamlit App Configuration
st.set_page_config(
    page_title="Cricket Match Scraper",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #1f4e79, #2d5aa0);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 10px 10px;
    }
    
    .match-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2d5aa0;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .score-highlight {
        background: #e8f5e8;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
        color: #2d5aa0;
    }
    
    .status-live {
        background: #28a745;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .debug-info {
        background: #f1f3f4;
        padding: 1rem;
        border-radius: 8px;
        font-family: monospace;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Main App
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏏 Enhanced Cricket Match Scraper</h1>
        <p>Live Cricket Scores & Match Information</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize scraper
    scraper = CricketScraper()
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎯 Team Selection")
        team1 = st.selectbox("Team 1", ["India", "Australia", "England", "Pakistan", "South Africa", "New Zealand"], index=0)
        team2 = st.selectbox("Team 2", ["Australia", "India", "England", "Pakistan", "South Africa", "New Zealand"], index=0)
        
        st.header("⚙️ Search Settings")
        auto_refresh = st.checkbox("Auto Refresh", value=False)
        if auto_refresh:
            refresh_interval = st.slider("Refresh Interval (seconds)", 30, 300, 60)
        
        st.header("📊 Data Sources")
        source_cricbuzz = st.checkbox("Cricbuzz", value=True)
        source_espn = st.checkbox("ESPNCricinfo", value=True)
        
        st.header("🔍 Additional Options")
        show_general_data = st.checkbox("Show General Cricket Data", value=True)
        show_debug = st.checkbox("Show Debug Info", value=False)
        verbose_output = st.checkbox("Verbose Output", value=True)
    
    # Main search button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"🔍 Search {team1} vs {team2} Matches", type="primary", use_container_width=True):
            search_matches(scraper, team1, team2, source_cricbuzz, source_espn, show_general_data, show_debug, verbose_output)
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

def search_matches(scraper, team1, team2, use_cricbuzz, use_espn, show_general, show_debug, verbose):
    """Search and display matches with enhanced output"""
    
    with st.spinner(f"🔍 Searching for {team1} vs {team2} matches..."):
        all_matches = []
        
        if verbose:
            st.write("### 📋 Search Progress")
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Search Cricbuzz
        if use_cricbuzz:
            status_text.text("Checking Cricbuzz...")
            progress_bar.progress(25)
            
            with st.expander("🔍 Cricbuzz Search Details", expanded=verbose):
                cricbuzz_matches = scraper.scrape_cricbuzz_live(team1, team2)
                all_matches.extend(cricbuzz_matches)
                st.write(f"Found {len(cricbuzz_matches)} matches from Cricbuzz")
        
        # Search ESPNCricinfo
        if use_espn:
            status_text.text("Checking ESPNCricinfo...")
            progress_bar.progress(50)
            
            with st.expander("🔍 ESPNCricinfo Search Details", expanded=verbose):
                espn_matches = scraper.scrape_espn_live(team1, team2)
                all_matches.extend(espn_matches)
                st.write(f"Found {len(espn_matches)} matches from ESPNCricinfo")
        
        progress_bar.progress(75)
        status_text.text("Processing results...")
        
        # Clear progress indicators
        progress_bar.progress(100)
        time.sleep(0.5)
        progress_bar.empty()
        status_text.empty()
    
    # Display results
    display_enhanced_results(all_matches, scraper, show_general, show_debug, team1, team2)

def display_enhanced_results(matches, scraper, show_general, show_debug, team1, team2):
    """Display search results with enhanced formatting"""
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Matches Found", len(matches))
    
    with col2:
        sources = list(set([match['source'] for match in matches])) if matches else []
        st.metric("Sources", len(sources) if sources else 0)
    
    with col3:
        st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
    
    with col4:
        st.metric("Status", "🟢 Active" if matches else "🔴 Searching")
    
    st.divider()
    
    # Match results
    if matches:
        st.success(f"✅ Found {len(matches)} {team1} vs {team2} match(es)")
        
        for i, match in enumerate(matches, 1):
            with st.container():
                st.markdown(f"""
                <div class="match-card">
                    <h4>🏏 Match {i} - {match['source']}</h4>
                    <p><strong>Teams:</strong> {match['teams']}</p>
                    <div class="score-highlight">
                        <strong>Scores:</strong> {match.get('scores', 'Not available')}
                    </div>
                    <p><strong>Status:</strong> <span class="status-live">{match.get('status', 'Unknown')}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                if match.get('url'):
                    st.link_button(f"📺 Watch Match {i}", match['url'])
                
                # Show full text if available
                if match.get('full_text') and len(match['full_text']) > 50:
                    with st.expander(f"📄 Full Match Details {i}"):
                        st.text(match['full_text'])
                
                st.write("")
    
    else:
        st.warning(f"❌ No live {team1} vs {team2} matches found")
        
        if show_general:
            with st.expander("🔍 General Cricket Data", expanded=True):
                st.info("Fetching general cricket data...")
                
                with st.spinner("Loading..."):
                    general_data = scraper.scrape_any_cricket_data()
                
                if general_data:
                    st.success(f"Found {len(general_data)} cricket-related items")
                    
                    # Group by type
                    data_by_type = {}
                    for item in general_data:
                        item_type = item.get('type', 'General')
                        if item_type not in data_by_type:
                            data_by_type[item_type] = []
                        data_by_type[item_type].append(item)
                    
                    # Display by type
                    for data_type, items in data_by_type.items():
                        st.subheader(f"📊 {data_type}")
                        for item in items[:5]:  # Show top 5 per type
                            st.markdown(f"- {item.get('text', 'No text')}")
                            if item.get('url'):
                                st.markdown(f"  🔗 [Link]({item['url']})")
                else:
                    st.error("No general cricket data found")
    
    # Debug information
    if show_debug:
        with st.expander("🔧 Debug Information"):
            st.subheader("Website Analysis")
            
            debug_sites = [
                "https://www.espncricinfo.com/live-cricket-score",
                "https://www.cricbuzz.com/cricket-match/live-scores"
            ]
            
            for site in debug_sites:
                st.write(f"**{site}:**")
                debug_info = scraper.debug_page_structure(site)
                
                if 'error' in debug_info:
                    st.error(f"Error: {debug_info['error']}")
                else:
                    st.markdown(f"""
                    <div class="debug-info">
                    Status Code: {debug_info.get('status_code', 'N/A')}<br>
                    Title: {debug_info.get('title', 'N/A')}<br>
                    Match Divs: {debug_info.get('match_divs', 0)}<br>
                    Total Divs: {debug_info.get('all_divs_count', 0)}<br>
                    Cricket Terms Found: {', '.join(debug_info.get('cricket_terms', []))}
                    </div>
                    """, unsafe_allow_html=True)
                st.write("")

# Footer
def show_footer():
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #6c757d; padding: 1rem;">
            🏏 Enhanced Cricket Match Scraper | Better Search & Display | Last updated: {}
        </div>
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        unsafe_allow_html=True
    )

# Run the app
if __name__ == "__main__":
    main()
    show_footer()