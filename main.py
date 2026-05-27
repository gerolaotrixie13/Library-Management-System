"""Main module demonstrating the Library Management System."""

from library_service import LibraryService
from exceptions import (
    BookNotAvailableException,
    BookNotFoundException,
    MemberNotFoundException,
    InvalidLoanException,
    MemberNotEligibleException,
    DuplicateBookException,
    DuplicateMemberException
)


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
