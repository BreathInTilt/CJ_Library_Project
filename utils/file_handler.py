import csv
from models.user import User
from models.book import Book
from models.loan import Loan
from datetime import datetime

def read_users():
    users = []
    try:
        with open('data/users.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)  # Skip header
            for row in reader:
                users.append(User(row[0], row[1], row[2]))
    except FileNotFoundError:
        pass
    return users

def write_users(users):
    with open('data/users.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['username', 'password', 'role'])
        for user in users:
            writer.writerow([user.username, user.password, user.role])

def read_books():
    books = []
    try:
        with open('data/books.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)  # Skip header
            for row in reader:
                books.append(Book(row[0], row[1], row[2], int(row[3]), float(row[4])))
    except FileNotFoundError:
        pass
    return books

def write_books(books):
    with open('data/books.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['id', 'title', 'author', 'copies', 'rating'])
        for book in books:
            writer.writerow([book.id, book.title, book.author, book.copies, book.rating])

def read_loans():
    loans = []
    try:
        with open('data/loans.csv', 'r') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)
            for row in reader:
                loan_date = datetime.fromisoformat(row[2])
                return_date = datetime.fromisoformat(row[3]) if row[3] else None
                loans.append(Loan(row[0], row[1], loan_date, return_date))
    except FileNotFoundError:
        pass
    return loans

def write_loans(loans):
    with open('data/loans.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['username', 'book_id', 'loan_date', 'return_date'])
        for loan in loans:
            writer.writerow([loan.username, loan.book_id, loan.loan_date.isoformat(),
                           loan.return_date.isoformat() if loan.return_date else ''])