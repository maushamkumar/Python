# Library Management System

A comprehensive console-based library management system built with Python that allows administrators to manage books and users, handle book transactions, and provides basic user functionality for searching books and viewing account information.

## Features

### Administrator Features
- **Book Management**
  - Add new books with details (ID, name, author, copies, price)
  - Edit existing book information
  - Delete books from the system
  - View all books in a formatted table

- **User Management**
  - Add new users to the system
  - Edit user information
  - Delete users from the system
  - View all registered users

- **Book Transactions**
  - Issue books to users (15-day lending period)
  - Process book returns with automatic fine calculation
  - Track book availability and user borrowing status

### User Features
- Search for books by name (partial matching)
- View personal account information and borrowing status

## Installation

### Prerequisites
- Python 3.6 or higher
- No additional packages required (uses only standard library)

### Setup
1. Clone or download the repository
2. Navigate to the project directory
3. Run the program:
   ```bash
   python app.py
```

# Usage
### Getting Started
- Run the program

- Enter the main system password: `libpass`

- Choose between Administrator or User access

### Administrator Access
- Password: `library`

- Full access to all system features including book/user management and transactions

### User Access
- No additional password required

- Limited access to search and personal information features

### Data Storage
- Books are stored in books.json

- Users are stored in users.json

- Data is automatically saved after each operation

- Files are created automatically on first use

# System Structure
### Book Information
Each book contains:

- ID: Unique identifier

- Name: Book title

- Author: Author name

- Copies: Total number of copies

- Copies Left: Available copies for lending

- Price: Book price

### User Information
- Each user contains:

- ID: Unique identifier

- Name: User's full name

- Book ID: Currently borrowed book (0 if none)

- Issue Date: Date when book was borrowed

- Due Date: Return deadline (15 days from issue)

# Key Features
### Authentication System
- Two-tier password protection

- 3 attempts allowed for each authentication

- Secure password input (hidden from display)

### Fine Calculation
- ₹3 per day for overdue books

- Automatic calculation on book return

- Grace period until due date

### Data Persistence
- JSON-based storage system

- Automatic backup on each operation

- Error handling for file operations

### User Interface
- Clear, formatted console interface

- Contextual menus and navigation

- Real-time date/time display

- Screen clearing for better user experience

# Menu Structure

 ```bash
 Main Menu
├── Administrator
│   ├── Add/Edit Book
│   │   ├── Add Book
│   │   ├── Edit Book Details
│   │   └── Delete Book
│   ├── Add/Edit User
│   │   ├── Add User
│   │   ├── Edit User Details
│   │   └── Delete User
│   ├── List Books
│   ├── List Users
│   ├── Issue Book
│   └── Collect Book
└── User
    ├── Search Book
    └── User Info
```

# File Structure

```bash
library_management/
├── library_management.py    # Main program file
├── books.json               # Book data storage (auto-generated)
├── users.json               # User data storage (auto-generated)
└── README.md                # This file
```