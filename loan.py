"""Loan class for the Library Management System."""

from datetime import datetime, timedelta
from typing import Optional


class Loan:
    """Represents a loan record of a book to a member."""

    # Class variable for loan duration (in days)
    LOAN_DURATION_DAYS = 14
    LATE_FEE_PER_DAY = 1.0  # Currency units per day

    def __init__(self, loan_id: str, member_id: str, book_id: str, 
                 borrow_date: datetime = None, return_date: Optional[datetime] = None):
        """Initialize a Loan.
        
        Args:
            loan_id: Unique identifier for the loan
            member_id: ID of the member borrowing the book
            book_id: ID of the book being borrowed
            borrow_date: Date of borrowing (defaults to now)
            return_date: Date of return (None if not yet returned)
        """
        self.loan_id = loan_id
        self.member_id = member_id
        self.book_id = book_id
        self.borrow_date = borrow_date or datetime.now()
        self.return_date = return_date
        self.due_date = self.borrow_date + timedelta(days=self.LOAN_DURATION_DAYS)
        self.is_returned = return_date is not None
        self.late_fee = 0.0

    def calculate_due_date(self) -> datetime:
        """Calculate the due date for the loan.
        
        Returns:
            Due date as datetime object
        """
        return self.borrow_date + timedelta(days=self.LOAN_DURATION_DAYS)

    def is_overdue(self) -> bool:
        """Check if the loan is overdue.
        
        Returns:
            True if the current date is past the due date and book not returned, False otherwise
        """
        if self.is_returned:
            return False
        return datetime.now() > self.due_date

    def get_days_overdue(self) -> int:
        """Get the number of days the loan is overdue.
        
        Returns:
            Number of days overdue (0 if not overdue)
        """
        if not self.is_overdue():
            return 0
        return (datetime.now() - self.due_date).days

    def calculate_late_fee(self) -> float:
        """Calculate late fees for overdue books.
        
        Returns:
            Late fee amount
        """
        days_overdue = self.get_days_overdue()
        self.late_fee = days_overdue * self.LATE_FEE_PER_DAY
        return self.late_fee

    def return_book(self) -> None:
        """Mark the book as returned and calculate fees."""
        self.return_date = datetime.now()
        self.is_returned = True
        self.calculate_late_fee()

    def get_loan_details(self) -> dict:
        """Get detailed information about the loan.
        
        Returns:
            Dictionary containing loan information
        """
        return {
            'loan_id': self.loan_id,
            'member_id': self.member_id,
            'book_id': self.book_id,
            'borrow_date': self.borrow_date.strftime('%Y-%m-%d %H:%M:%S'),
            'due_date': self.due_date.strftime('%Y-%m-%d'),
            'return_date': self.return_date.strftime('%Y-%m-%d %H:%M:%S') if self.return_date else 'Not returned',
            'is_returned': self.is_returned,
            'is_overdue': self.is_overdue(),
            'days_overdue': self.get_days_overdue(),
            'late_fee': round(self.calculate_late_fee(), 2)
        }

    def __str__(self) -> str:
        """String representation of the loan."""
        status = "Returned" if self.is_returned else ("Overdue" if self.is_overdue() else "Active")
        return f"Loan(ID: {self.loan_id}, Member: {self.member_id}, Book: {self.book_id}, Status: {status})"

    def __repr__(self) -> str:
        """Representation of the loan."""
        return self.__str__()
