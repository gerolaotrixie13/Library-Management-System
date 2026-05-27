"""Library Service class that manages the Library Management System operations."""

from typing import List, Optional, Dict
from datetime import datetime
from book import Book
from member import Member
from loan import Loan
from exceptions import (
    BookNotAvailableException,
    BookNotFoundException,
    MemberNotFoundException,
    InvalidLoanException,
    MemberNotEligibleException,
    DuplicateBookException,
    DuplicateMemberException
)


class LibraryService:
    """Service class managing all library operations."""

    def __init__(self, library_name: str):
        """Initialize the Library Service.
        
        Args:
            library_name: Name of the library
        """
        self.library_name = library_name
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.loans: Dict[str, Loan] = {}
        self.loan_counter = 0

    # ==================== BOOK MANAGEMENT ====================

    def add_book(self, book_id: str, title: str, author: str, isbn: str,
                 publication_year: int, total_copies: int) -> Book:
        """Add a new book to the library.
        
        Args:
            book_id: Unique identifier for the book
            title: Title of the book
            author: Author of the book
            isbn: ISBN of the book
            publication_year: Year of publication
            total_copies: Total number of copies
            
        Returns:
            The added Book object
            
        Raises:
            DuplicateBookException: If book with same ID already exists
        """
        if book_id in self.books:
            raise DuplicateBookException(f"Book with ID '{book_id}' already exists.")
        
        book = Book(book_id, title, author, isbn, publication_year, total_copies)
        self.books[book_id] = book
        return book

    def get_book(self, book_id: str) -> Book:
        """Get a book by its ID.
        
        Args:
            book_id: ID of the book
            
        Returns:
            The Book object
            
        Raises:
            BookNotFoundException: If book is not found
        """
        if book_id not in self.books:
            raise BookNotFoundException(f"Book with ID '{book_id}' not found.")
        return self.books[book_id]

    def search_books_by_title(self, title: str) -> List[Book]:
        """Search for books by title (partial match).
        
        Args:
            title: Title to search for
            
        Returns:
            List of matching Book objects
        """
        return [book for book in self.books.values() 
                if title.lower() in book.title.lower()]

    def search_books_by_author(self, author: str) -> List[Book]:
        """Search for books by author (partial match).
        
        Args:
            author: Author name to search for
            
        Returns:
            List of matching Book objects
        """
        return [book for book in self.books.values() 
                if author.lower() in book.author.lower()]

    def list_all_books(self) -> List[Book]:
        """Get all books in the library.
        
        Returns:
            List of all Book objects
        """
        return list(self.books.values())

    def list_available_books(self) -> List[Book]:
        """Get all available books in the library.
        
        Returns:
            List of available Book objects
        """
        return [book for book in self.books.values() if book.is_available()]

    # ==================== MEMBER MANAGEMENT ====================

    def add_member(self, member_id: str, name: str, email: str, phone: str) -> Member:
        """Add a new member to the library.
        
        Args:
            member_id: Unique identifier for the member
            name: Name of the member
            email: Email of the member
            phone: Phone number of the member
            
        Returns:
            The added Member object
            
        Raises:
            DuplicateMemberException: If member with same ID already exists
        """
        if member_id in self.members:
            raise DuplicateMemberException(f"Member with ID '{member_id}' already exists.")
        
        member = Member(member_id, name, email, phone)
        self.members[member_id] = member
        return member

    def get_member(self, member_id: str) -> Member:
        """Get a member by their ID.
        
        Args:
            member_id: ID of the member
            
        Returns:
            The Member object
            
        Raises:
            MemberNotFoundException: If member is not found
        """
        if member_id not in self.members:
            raise MemberNotFoundException(f"Member with ID '{member_id}' not found.")
        return self.members[member_id]

    def search_members_by_name(self, name: str) -> List[Member]:
        """Search for members by name (partial match).
        
        Args:
            name: Name to search for
            
        Returns:
            List of matching Member objects
        """
        return [member for member in self.members.values() 
                if name.lower() in member.name.lower()]

    def list_all_members(self) -> List[Member]:
        """Get all members in the library.
        
        Returns:
            List of all Member objects
        """
        return list(self.members.values())

    def list_active_members(self) -> List[Member]:
        """Get all active members in the library.
        
        Returns:
            List of active Member objects
        """
        return [member for member in self.members.values() if member.is_active]

    def deactivate_member(self, member_id: str) -> None:
        """Deactivate a member's membership.
        
        Args:
            member_id: ID of the member to deactivate
            
        Raises:
            MemberNotFoundException: If member is not found
        """
        member = self.get_member(member_id)
        member.deactivate_membership()

    def activate_member(self, member_id: str) -> None:
        """Activate a member's membership.
        
        Args:
            member_id: ID of the member to activate
            
        Raises:
            MemberNotFoundException: If member is not found
        """
        member = self.get_member(member_id)
        member.activate_membership()

    # ==================== LOAN MANAGEMENT ====================

    def borrow_book(self, member_id: str, book_id: str) -> Loan:
        """Process borrowing a book by a member.
        
        Args:
            member_id: ID of the member borrowing the book
            book_id: ID of the book to borrow
            
        Returns:
            The created Loan object
            
        Raises:
            MemberNotFoundException: If member is not found
            BookNotFoundException: If book is not found
            MemberNotEligibleException: If member is not active
            BookNotAvailableException: If book is not available
        """
        member = self.get_member(member_id)
        book = self.get_book(book_id)
        
        if not member.is_active:
            raise MemberNotEligibleException(
                f"Member '{member_id}' is not active and cannot borrow books."
            )
        
        book.borrow_book()  # This raises BookNotAvailableException if needed
        member.borrow_book(book_id)
        
        # Create loan record
        self.loan_counter += 1
        loan_id = f"LOAN_{self.loan_counter:05d}"
        loan = Loan(loan_id, member_id, book_id)
        self.loans[loan_id] = loan
        
        return loan

    def return_book(self, loan_id: str) -> Dict:
        """Process returning a borrowed book.
        
        Args:
            loan_id: ID of the loan
            
        Returns:
            Dictionary with return details including late fees if any
            
        Raises:
            InvalidLoanException: If loan is not found or already returned
        """
        if loan_id not in self.loans:
            raise InvalidLoanException(f"Loan with ID '{loan_id}' not found.")
        
        loan = self.loans[loan_id]
        
        if loan.is_returned:
            raise InvalidLoanException(f"Loan '{loan_id}' has already been returned.")
        
        member = self.get_member(loan.member_id)
        book = self.get_book(loan.book_id)
        
        loan.return_book()
        member.return_book(loan.book_id)
        book.return_book()
        
        return {
            'loan_id': loan_id,
            'member_id': loan.member_id,
            'book_id': loan.book_id,
            'return_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_overdue': loan.get_days_overdue() > 0,
            'days_overdue': loan.get_days_overdue(),
            'late_fee': round(loan.calculate_late_fee(), 2)
        }

    def get_loan(self, loan_id: str) -> Loan:
        """Get a loan record by its ID.
        
        Args:
            loan_id: ID of the loan
            
        Returns:
            The Loan object
            
        Raises:
            InvalidLoanException: If loan is not found
        """
        if loan_id not in self.loans:
            raise InvalidLoanException(f"Loan with ID '{loan_id}' not found.")
        return self.loans[loan_id]

    def get_active_loans(self) -> List[Loan]:
        """Get all active (not returned) loans.
        
        Returns:
            List of active Loan objects
        """
        return [loan for loan in self.loans.values() if not loan.is_returned]

    def get_overdue_loans(self) -> List[Loan]:
        """Get all overdue loans.
        
        Returns:
            List of overdue Loan objects
        """
        return [loan for loan in self.loans.values() if loan.is_overdue()]

    def get_member_loans(self, member_id: str) -> List[Loan]:
        """Get all loans for a specific member.
        
        Args:
            member_id: ID of the member
            
        Returns:
            List of Loan objects for the member
            
        Raises:
            MemberNotFoundException: If member is not found
        """
        self.get_member(member_id)  # Verify member exists
        return [loan for loan in self.loans.values() if loan.member_id == member_id]

    def get_member_active_loans(self, member_id: str) -> List[Loan]:
        """Get all active loans for a specific member.
        
        Args:
            member_id: ID of the member
            
        Returns:
            List of active Loan objects for the member
            
        Raises:
            MemberNotFoundException: If member is not found
        """
        self.get_member(member_id)  # Verify member exists
        return [loan for loan in self.loans.values() 
                if loan.member_id == member_id and not loan.is_returned]

    # ==================== STATISTICS ====================

    def get_library_statistics(self) -> Dict:
        """Get statistics about the library.
        
        Returns:
            Dictionary containing library statistics
        """
        total_books = sum(book.total_copies for book in self.books.values())
        available_books = sum(book.available_copies for book in self.books.values())
        borrowed_books = total_books - available_books
        active_loans = len(self.get_active_loans())
        overdue_loans = len(self.get_overdue_loans())
        total_late_fees = sum(loan.calculate_late_fee() for loan in self.loans.values())
        
        return {
            'library_name': self.library_name,
            'total_unique_books': len(self.books),
            'total_book_copies': total_books,
            'available_copies': available_books,
            'borrowed_copies': borrowed_books,
            'total_members': len(self.members),
            'active_members': len(self.list_active_members()),
            'total_loans': len(self.loans),
            'active_loans': active_loans,
            'overdue_loans': overdue_loans,
            'total_late_fees': round(total_late_fees, 2)
        }

    def __str__(self) -> str:
        """String representation of the library service."""
        stats = self.get_library_statistics()
        return f"{self.library_name} - Books: {stats['total_unique_books']}, Members: {stats['total_members']}, Active Loans: {stats['active_loans']}"
