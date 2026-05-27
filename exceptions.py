"""Custom exceptions for the Library Management System."""


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
