"""
Custom exception classes for the inventory management system.
"""
from typing import Any, Dict, Optional


class InventoryManagementException(Exception):
    """Base exception class for inventory management system."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(InventoryManagementException):
    """Raised when authentication fails."""
    pass


class AuthorizationError(InventoryManagementException):
    """Raised when user lacks required permissions."""
    pass


class ValidationError(InventoryManagementException):
    """Raised when input validation fails."""
    pass


class DatabaseError(InventoryManagementException):
    """Raised when database operations fail."""
    pass


class BusinessLogicError(InventoryManagementException):
    """Raised when business logic constraints are violated."""
    pass


class ResourceNotFoundError(InventoryManagementException):
    """Raised when a requested resource is not found."""
    pass


class ResourceConflictError(InventoryManagementException):
    """Raised when a resource conflict occurs (e.g., duplicate email)."""
    pass


class InsufficientStockError(BusinessLogicError):
    """Raised when there's insufficient stock for an operation."""
    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when login credentials are invalid."""
    pass


class TokenExpiredError(AuthenticationError):
    """Raised when JWT token has expired."""
    pass


class InvalidTokenError(AuthenticationError):
    """Raised when JWT token is invalid or malformed."""
    pass


class UnauthorizedRoleError(AuthorizationError):
    """Raised when user role is not authorized for the operation."""
    pass


class UserNotActiveError(AuthenticationError):
    """Raised when user account is not active."""
    pass


class EmailNotInvitedError(AuthorizationError):
    """Raised when email is not invited for registration."""
    pass


class DuplicateEmailError(ResourceConflictError):
    """Raised when attempting to create user with existing email."""
    pass