from datetime import datetime, timedelta
from collections import defaultdict
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def calculate_average_rating(books):
    if not books:
        return 0
    return sum(book.rating for book in books) / len(books)


def generate_loan_statistics(loans):
    logger.debug(f"Processing {len(loans)} loans")
    daily_loans = defaultdict(int)
    daily_returns = defaultdict(int)
    start_date = datetime.now() - timedelta(days=30)
    logger.debug(f"Start date for statistics: {start_date}")

    # Generate all dates in the last 30 days for consistent x-axis
    all_dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(31)]

    # Process loans and returns
    for loan in loans:
        loan_date_str = loan.loan_date.strftime('%Y-%m-%d')
        if loan.loan_date >= start_date:
            daily_loans[loan_date_str] += 1
            logger.debug(f"Loan: username={loan.username}, book_id={loan.book_id}, loan_date={loan.loan_date}")

        if loan.return_date and loan.return_date >= start_date:
            return_date_str = loan.return_date.strftime('%Y-%m-%d')
            daily_returns[return_date_str] += 1
            logger.debug(f"Return: username={loan.username}, book_id={loan.book_id}, return_date={loan.return_date}")

    # Ensure all dates have an entry (0 if no loans/returns)
    loan_data = {date: daily_loans.get(date, 0) for date in all_dates}
    return_data = {date: daily_returns.get(date, 0) for date in all_dates}

    logger.debug(f"Daily loans: {dict(loan_data)}")
    logger.debug(f"Daily returns: {dict(return_data)}")
    return loan_data, return_data, all_dates