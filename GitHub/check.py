import sys 
import requests
import json

def get_github_activity(username):
    """Fetch GitHub activity for a user"""
    response = requests.get((f"https://api.github.com/users/{username}/events"))
    
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error: {response.status_code}")
        
    return data

def show_usage():
        """Show usage instructions"""
        usage = """
Task Tracker CLI

Usage:
    python check.py <username>

Examples:
    python check.py maushamkumar
        """
        return usage
        
def main():
    if len(sys.argv) < 2:
        print(show_usage())
        return
        
if __name__ == "__main__":
    main()
    

