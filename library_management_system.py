"""
Consolidated Library Management System - All code in one file.
This file contains all the classes and functionality for the Library Management System.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict


# ==================== CUSTOM EXCEPTIONS ====================

class LibraryException(Exception):
    """Base exception for all library-related errors."""
    pass


class BookNotAvailableException(LibraryException):
    """Raised when a book is not available for borrowing."""
    pass


class BookNotFoundException(LibraryException):
    """Raised when a book is not found in the library."""
    pass


class MemberNotFoundException(LibraryException):
    """Raised when a member is not found in the library system."""
    pass


class InvalidLoanException(LibraryException):
    """Raised when an invalid loan operation is attempted."""
    pass


class MemberNotEligibleException(LibraryException):
    """Raised when a member is not eligible to borrow books."""
    pass


class DuplicateBookException(LibraryException):
    """Raised when attempting to add a duplicate book."""
    pass


class DuplicateMemberException(LibraryException):
    """Raised when attempting to add a duplicate member."""
    pass


# ==================== BOOK CLASS ====================

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


# ==================== MEMBER CLASS ====================

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


# ==================== LOAN CLASS ====================

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


# ==================== LIBRARY SERVICE CLASS ====================

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


# ==================== MAIN DEMONSTRATION ====================

def print_header(title: str) -> None:
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def print_subheader(title: str) -> None:
    """Print a formatted subheader."""
    print(f"\n{'-'*60}")
    print(f" {title}")
    print(f"-"*60)


def display_book_details(book):
    """Display book details in a formatted way."""
    details = book.get_book_details()
    print(f"  Book ID: {details['book_id']}")
    print(f"  Title: {details['title']}")
    print(f"  Author: {details['author']}")
    print(f"  ISBN: {details['isbn']}")
    print(f"  Publication Year: {details['publication_year']}")
    print(f"  Available/Total: {details['available_copies']}/{details['total_copies']}")


def display_member_details(member):
    """Display member details in a formatted way."""
    details = member.get_member_details()
    print(f"  Member ID: {details['member_id']}")
    print(f"  Name: {details['name']}")
    print(f"  Email: {details['email']}")
    print(f"  Phone: {details['phone']}")
    print(f"  Status: {'Active' if details['is_active'] else 'Inactive'}")
    print(f"  Books Borrowed: {details['total_borrowed']}")


def display_loan_details(loan):
    """Display loan details in a formatted way."""
    details = loan.get_loan_details()
    print(f"  Loan ID: {details['loan_id']}")
    print(f"  Member ID: {details['member_id']}")
    print(f"  Book ID: {details['book_id']}")
    print(f"  Borrow Date: {details['borrow_date']}")
    print(f"  Due Date: {details['due_date']}")
    print(f"  Return Date: {details['return_date']}")
    print(f"  Status: {'Returned' if details['is_returned'] else ('Overdue' if details['is_overdue'] else 'Active')}")
    if details['days_overdue'] > 0:
        print(f"  Days Overdue: {details['days_overdue']}")
        print(f"  Late Fee: ${details['late_fee']}")


def main():
    """Main function demonstrating the Library Management System."""
    
    print_header("LIBRARY MANAGEMENT SYSTEM")
    
    # Initialize the library service
    library = LibraryService("City Central Library")
    print(f"\n✓ Library initialized: {library.library_name}")
    
    # ==================== ADD BOOKS ====================
    print_subheader("1. ADDING BOOKS")
    
    try:
        book1 = library.add_book("B001", "Python Programming", "Guido van Rossum", "978-0-13-404266-9", 2009, 5)
        print(f"✓ Added: {book1}")
        
        book2 = library.add_book("B002", "The Great Gatsby", "F. Scott Fitzgerald", "978-0-7432-7356-5", 1925, 3)
        print(f"✓ Added: {book2}")
        
        book3 = library.add_book("B003", "To Kill a Mockingbird", "Harper Lee", "978-0-06-112008-4", 1960, 4)
        print(f"✓ Added: {book3}")
        
        book4 = library.add_book("B004", "1984", "George Orwell", "978-0-452-26423-9", 1949, 2)
        print(f"✓ Added: {book4}")
        
        book5 = library.add_book("B005", "Data Science Handbook", "Jake VanderPlas", "978-1-491-91205-8", 2016, 3)
        print(f"✓ Added: {book5}")
        
    except DuplicateBookException as e:
        print(f"✗ Error: {e}")
    
    # ==================== ADD MEMBERS ====================
    print_subheader("2. ADDING MEMBERS")
    
    try:
        member1 = library.add_member("M001", "Alice Johnson", "alice@email.com", "555-0001")
        print(f"✓ Added: {member1}")
        
        member2 = library.add_member("M002", "Bob Smith", "bob@email.com", "555-0002")
        print(f"✓ Added: {member2}")
        
        member3 = library.add_member("M003", "Charlie Brown", "charlie@email.com", "555-0003")
        print(f"✓ Added: {member3}")
        
        member4 = library.add_member("M004", "Diana Prince", "diana@email.com", "555-0004")
        print(f"✓ Added: {member4}")
        
    except DuplicateMemberException as e:
        print(f"✗ Error: {e}")
    
    # ==================== SEARCH BOOKS ====================
    print_subheader("3. SEARCHING BOOKS")
    
    print("\nSearching by title 'Python':")
    results = library.search_books_by_title("Python")
    for book in results:
        display_book_details(book)
    
    print("\nSearching by author 'George Orwell':")
    results = library.search_books_by_author("George Orwell")
    for book in results:
        display_book_details(book)
    
    # ==================== SEARCH MEMBERS ====================
    print_subheader("4. SEARCHING MEMBERS")
    
    print("\nSearching by name 'Johnson':")
    results = library.search_members_by_name("Johnson")
    for member in results:
        display_member_details(member)
    
    # ==================== BORROW BOOKS ====================
    print_subheader("5. BORROWING BOOKS")
    
    try:
        loan1 = library.borrow_book("M001", "B001")
        print(f"✓ {library.get_member('M001').name} borrowed 'Python Programming'")
        print(f"  Loan ID: {loan1.loan_id}")
        print(f"  Due Date: {loan1.due_date.strftime('%Y-%m-%d')}")
        
        loan2 = library.borrow_book("M001", "B002")
        print(f"✓ {library.get_member('M001').name} borrowed 'The Great Gatsby'")
        print(f"  Loan ID: {loan2.loan_id}")
        
        loan3 = library.borrow_book("M002", "B003")
        print(f"✓ {library.get_member('M002').name} borrowed 'To Kill a Mockingbird'")
        print(f"  Loan ID: {loan3.loan_id}")
        
        loan4 = library.borrow_book("M003", "B004")
        print(f"✓ {library.get_member('M003').name} borrowed '1984'")
        print(f"  Loan ID: {loan4.loan_id}")
        
        loan5 = library.borrow_book("M002", "B005")
        print(f"✓ {library.get_member('M002').name} borrowed 'Data Science Handbook'")
        print(f"  Loan ID: {loan5.loan_id}")
        
    except (MemberNotFoundException, BookNotFoundException, 
            BookNotAvailableException, MemberNotEligibleException) as e:
        print(f"✗ Error: {e}")
    
    # ==================== DISPLAY AVAILABLE BOOKS ====================
    print_subheader("6. AVAILABLE BOOKS")
    
    available = library.list_available_books()
    print(f"\nTotal available books: {len(available)}")
    for book in available:
        display_book_details(book)
    
    # ==================== DISPLAY MEMBER LOANS ====================
    print_subheader("7. MEMBER LOANS")
    
    print(f"\n{library.get_member('M001').name}'s loans:")
    loans = library.get_member_active_loans("M001")
    for loan in loans:
        display_loan_details(loan)
    
    # ==================== RETURN BOOKS ====================
    print_subheader("8. RETURNING BOOKS")
    
    try:
        result = library.return_book("LOAN_00001")
        print(f"✓ Book returned successfully")
        print(f"  Loan ID: {result['loan_id']}")
        print(f"  Return Date: {result['return_date']}")
        print(f"  Late Fee: ${result['late_fee']}")
        
        result = library.return_book("LOAN_00002")
        print(f"✓ Book returned successfully")
        print(f"  Loan ID: {result['loan_id']}")
        
    except InvalidLoanException as e:
        print(f"✗ Error: {e}")
    
    # ==================== DISPLAY ACTIVE LOANS ====================
    print_subheader("9. ACTIVE LOANS")
    
    active_loans = library.get_active_loans()
    print(f"\nTotal active loans: {len(active_loans)}")
    for loan in active_loans:
        display_loan_details(loan)
    
    # ==================== MEMBER MANAGEMENT ====================
    print_subheader("10. MEMBER MANAGEMENT")
    
    print(f"\nDeactivating member M004...")
    library.deactivate_member("M004")
    print(f"✓ Member M004 deactivated")
    
    try:
        loan = library.borrow_book("M004", "B001")
    except MemberNotEligibleException as e:
        print(f"✓ Inactive member cannot borrow: {e}")
    
    print(f"\nActivating member M004...")
    library.activate_member("M004")
    print(f"✓ Member M004 activated")
    
    loan6 = library.borrow_book("M004", "B001")
    print(f"✓ Member M004 can now borrow books")
    
    # ==================== LIBRARY STATISTICS ====================
    print_subheader("11. LIBRARY STATISTICS")
    
    stats = library.get_library_statistics()
    print(f"\nLibrary: {stats['library_name']}")
    print(f"Total Unique Books: {stats['total_unique_books']}")
    print(f"Total Book Copies: {stats['total_book_copies']}")
    print(f"Available Copies: {stats['available_copies']}")
    print(f"Borrowed Copies: {stats['borrowed_copies']}")
    print(f"Total Members: {stats['total_members']}")
    print(f"Active Members: {stats['active_members']}")
    print(f"Total Loans: {stats['total_loans']}")
    print(f"Active Loans: {stats['active_loans']}")
    print(f"Overdue Loans: {stats['overdue_loans']}")
    print(f"Total Late Fees: ${stats['total_late_fees']}")
    
    # ==================== ALL BOOKS ====================
    print_subheader("12. ALL BOOKS IN LIBRARY")
    
    books = library.list_all_books()
    print(f"\nTotal books: {len(books)}")
    for book in books:
        display_book_details(book)
        print()
    
    # ==================== ALL MEMBERS ====================
    print_subheader("13. ALL MEMBERS IN LIBRARY")
    
    members = library.list_all_members()
    print(f"\nTotal members: {len(members)}")
    for member in members:
        display_member_details(member)
        print()
    
    print_header("END OF DEMONSTRATION")


if __name__ == "__main__":
    main()
