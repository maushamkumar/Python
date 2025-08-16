import os 
import sys
import argparse
import json 
from datetime import datetime

class ExpenseTracker:
    def __init__(self, filename='expenses.json'):
        self.filename = filename
        self.allowed_categories = ['food', 'transport', 'utilities', 'entertainment', 'other']
        
        
    def load_data(self):
        """Load expenses from JSON file"""
        
        if not os.path.exists(self.filename):
            return []
        try:
            
            with open(self.filename, 'r') as f:
                return json.load(f)
            
        except (json.JSONDecodeError, ValueError):
            print("Error loading data. The file may be corrupted.")
            return []
        
        
    def save_data(self, data):
        """Save expenses to JSON file
        
        Args: 
            data (list): List of expenses to save
            
        Returns: None"""
        
        try:
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving data: {e}")
            sys.exit(1)
        
    def get_next_id(self, data):
        """Get the next available ID for a new expense
        
        Args:
            data (list): List of existing expenses
            
        Returns: int: Next available ID
        
        """
        
        if not data: 
            return 1 
        return max(data['ID'] for data in data) + 1
    
    
    

            
    def add_expense(self, description, amount):
        """Add a new expense
        
        Args:
            description (str): Description of the expense
            amount (float): Amount of the expense
            
        Returns: None"""
        
        data = self.load_data()
        expense_id = self.get_next_id(data)
        
        new_expense = {
            "ID": expense_id,
            "description": description,
            "amount": amount,
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        data.append(new_expense)
        self.save_data(data)
        print(f"Expense added successfully (ID: {expense_id})")


    def show_usage(self):
        print("Run with --help to see usage.")


def main():
    tracker = ExpenseTracker()

    parser = argparse.ArgumentParser(description="Expense-tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add subcommand
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--description", required=True, help="Description of the expense")
    add_parser.add_argument("--amount", required=True, type=float, help="Amount of the expense")

    args = parser.parse_args()

    if args.command == "add":
        if args.amount < 0:
            print("Error: Expense cannot be negative.")
            sys.exit(1)
        tracker.add_expense(args.description, args.amount)
    else:
        tracker.show_usage()

if __name__ == "__main__":
    main()


