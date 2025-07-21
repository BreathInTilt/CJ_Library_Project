from datetime import datetime, timedelta

class Loan:
    def __init__(self, username, book_id, loan_date, return_date=None):
        self.username = username
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date

    def is_overdue(self):
        if self.return_date:
            return False
        return datetime.now() > self.loan_date + timedelta(days=14)