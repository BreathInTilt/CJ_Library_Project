from flask import Flask, render_template, request, redirect, url_for, flash, session
from models.user import User
from models.book import Book
from models.loan import Loan
from utils.file_handler import read_users, write_users, read_books, write_books, read_loans, write_loans
from utils.data_processor import calculate_average_rating, generate_loan_statistics
from datetime import datetime
import os
import json
#import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

app = Flask(__name__)
app.secret_key = "kapksdpakk2213"


users = read_users()
books = read_books()
loans = read_loans()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in users if u.username == username and u.password == password), None)
        if user:
            session['username'] = username
            session['role'] = user.role
            if user.role == 'librarian':
                return redirect(url_for('librarian_dashboard'))
            return redirect(url_for('member_dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if any(u.username == username for u in users):
            flash('Username already exists')
        else:
            users.append(User(username, password, role))
            write_users(users)
            flash('Registration successful')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/member_dashboard')
def member_dashboard():
    if 'username' not in session or session['role'] != 'member':
        return redirect(url_for('login'))
    # Get search query
    search_query = request.args.get('search_query', '').strip().lower()
    # Filter available books (copies > 0) by title or author
    available_books = [
        b for b in books if b.copies > 0 and
        (search_query in b.title.lower() or search_query in b.author.lower() or not search_query)
    ]
    user_loans = [l for l in loans if l.username == session['username'] and not l.return_date]
    borrowed_books = [next(b for b in books if b.id == l.book_id) for l in user_loans]
    return render_template('book_list.html', books=available_books, borrowed_books=borrowed_books, search_query=search_query)

@app.route('/librarian_dashboard')
def librarian_dashboard():
    if 'username' not in session or session['role'] != 'librarian':
        return redirect(url_for('login'))
    return render_template('librarian_dashboard.html')

@app.route('/loan_book/<book_id>', methods=['GET', 'POST'])
def loan_book(book_id):
    if 'username' not in session or session['role'] != 'member':
        return redirect(url_for('login'))
    book = next((b for b in books if b.id == book_id), None)
    if not book or book.copies <= 0:
        flash('Book not available')
        return redirect(url_for('member_dashboard'))
    if request.method == 'POST':
        loans.append(Loan(session['username'], book_id, datetime.now()))
        book.copies -= 1
        write_loans(loans)
        write_books(books)
        flash('Book borrowed successfully')
        return redirect(url_for('member_dashboard'))
    return render_template('loan_book.html', book=book)

@app.route('/return_book/<book_id>')
def return_book(book_id):
    if 'username' not in session or session['role'] != 'member':
        return redirect(url_for('login'))
    loan = next((l for l in loans if l.book_id == book_id and l.username == session['username'] and not l.return_date), None)
    if loan:
        loan.return_date = datetime.now()
        book = next(b for b in books if b.id == book_id)
        book.copies += 1
        write_loans(loans)
        write_books(books)
        flash('Book returned successfully')
    return redirect(url_for('member_dashboard'))

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'username' not in session or session['role'] != 'librarian':
        return redirect(url_for('login'))
    if request.method == 'POST':
        book_id = str(len(books) + 1)
        title = request.form['title']
        author = request.form['author']
        copies = int(request.form['copies'])
        rating = float(request.form['rating'])
        books.append(Book(book_id, title, author, copies, rating))
        write_books(books)
        flash('Book added successfully')
        return redirect(url_for('librarian_dashboard'))
    return render_template('add_book.html')

@app.route('/overdue_report')
def overdue_report():
    if 'username' not in session or session['role'] != 'librarian':
        return redirect(url_for('login'))
    overdue_loans = [l for l in loans if l.is_overdue()]
    return render_template('overdue_report.html', loans=overdue_loans)

@app.route('/statistics')
def statistics():
    if 'username' not in session or session['role'] != 'librarian':
        return redirect(url_for('login'))
    avg_rating = calculate_average_rating(books)
    daily_loans, daily_returns, all_dates = generate_loan_statistics(loans)
    # Create Plotly plot with multiple traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=all_dates,
        y=[daily_loans[date] for date in all_dates],
        name='Loans',
        line=dict(color='#007bff', width=2),
        marker=dict(size=8)
    ))
    fig.add_trace(go.Scatter(
        x=all_dates,
        y=[daily_returns[date] for date in all_dates],
        name='Returns',
        line=dict(color='#ff5733', width=2),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title='Library Activity: Loans and Returns (Last 30 Days)',
        xaxis_title='Date',
        yaxis_title='Count',
        yaxis=dict(tickmode='linear', tick0=0, dtick=1),
        xaxis=dict(tickangle=45),
        hovermode='x unified',
        legend=dict(x=0, y=1.1, orientation='h'),
        margin=dict(b=150),  # Space for rotated labels
        template='plotly_white'
    )
    plot_div = pyo.plot(fig, output_type='div', include_plotlyjs=False)
    daily_loan_data = {
        'labels': json.dumps(all_dates),
        'loan_values': json.dumps([daily_loans[date] for date in all_dates]),
        'return_values': json.dumps([daily_returns[date] for date in all_dates]),
        'plot_div': plot_div
    }
    return render_template('statistics.html', avg_rating=avg_rating, daily_loan_data=daily_loan_data)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)