"""Book class for the Library Management System."""

from datetime import datetime
from typing import Optional
from exceptions import BookNotAvailableException, InvalidLoanException


class Book:
    """Represents a book in the library."""

    def __init__(self, book_id: str, title: str, author: str, isbn: str, 
                 publication_year: int, total_copies: int):
        """Initialize a Book.
        
        Args:
            book_id: Unique identifier for the book
            title: Title of the book
            author: Author of the book
            isbn: ISBN of the book
            publication_year: Year of publication
            total_copies: Total number of copies available
        """
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year
        self.total_copies = total_copies
        self.available_copies = total_copies
        self.created_date = datetime.now()

    def is_available(self) -> bool:
        """Check if the book has available copies.
        
        Returns:
            True if available copies > 0, False otherwise
        """
        return self.available_copies > 0

    def borrow_book(self) -> None:
        """Reduce available copies when a book is borrowed.
        
        Raises:
            BookNotAvailableException: If no copies are available
        """
        if not self.is_available():
            raise BookNotAvailableException(
                f"Book '{self.title}' is not available for borrowing."
            )
        self.available_copies -= 1

    def return_book(self) -> None:
        """Increase available copies when a book is returned.
        
        Raises:
            InvalidLoanException: If all copies are already returned
        """
        if self.available_copies >= self.total_copies:
            raise InvalidLoanException(
                f"Cannot return more copies of '{self.title}' than were borrowed."
            )
        self.available_copies += 1

    def get_book_details(self) -> dict:
        """Get detailed information about the book.
        
        Returns:
            Dictionary containing book information
        """
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'publication_year': self.publication_year,
            'total_copies': self.total_copies,
            'available_copies': self.available_copies,
            'created_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S')
        }

    def __str__(self) -> str:
        """String representation of the book."""
        return f"Book(ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Available: {self.available_copies}/{self.total_copies})"

    def __repr__(self) -> str:
        """Representation of the book."""
        return self.__str__()
