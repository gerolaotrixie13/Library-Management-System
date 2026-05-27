"""Member class for the Library Management System."""

from datetime import datetime
from typing import List


class Member:
    """Represents a member of the library."""

    def __init__(self, member_id: str, name: str, email: str, phone: str, 
                 membership_date: datetime = None):
        """Initialize a Member.
        
        Args:
            member_id: Unique identifier for the member
            name: Name of the member
            email: Email address of the member
            phone: Phone number of the member
            membership_date: Date of membership (defaults to now)
        """
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.membership_date = membership_date or datetime.now()
        self.borrowed_books: List[str] = []  # List of book_ids
        self.is_active = True

    def borrow_book(self, book_id: str) -> None:
        """Add a book to member's borrowed list.
        
        Args:
            book_id: ID of the book being borrowed
        """
        if book_id not in self.borrowed_books:
            self.borrowed_books.append(book_id)

    def return_book(self, book_id: str) -> None:
        """Remove a book from member's borrowed list.
        
        Args:
            book_id: ID of the book being returned
        """
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)

    def get_borrowed_books(self) -> List[str]:
        """Get list of books currently borrowed by the member.
        
        Returns:
            List of book IDs
        """
        return self.borrowed_books.copy()

    def has_borrowed_book(self, book_id: str) -> bool:
        """Check if member has borrowed a specific book.
        
        Args:
            book_id: ID of the book to check
            
        Returns:
            True if member has borrowed the book, False otherwise
        """
        return book_id in self.borrowed_books

    def get_member_details(self) -> dict:
        """Get detailed information about the member.
        
        Returns:
            Dictionary containing member information
        """
        return {
            'member_id': self.member_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'membership_date': self.membership_date.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': self.is_active,
            'borrowed_books': self.borrowed_books.copy(),
            'total_borrowed': len(self.borrowed_books)
        }

    def deactivate_membership(self) -> None:
        """Deactivate the member's membership."""
        self.is_active = False

    def activate_membership(self) -> None:
        """Activate the member's membership."""
        self.is_active = True

    def __str__(self) -> str:
        """String representation of the member."""
        return f"Member(ID: {self.member_id}, Name: {self.name}, Borrowed: {len(self.borrowed_books)}, Active: {self.is_active})"

    def __repr__(self) -> str:
        """Representation of the member."""
        return self.__str__()
