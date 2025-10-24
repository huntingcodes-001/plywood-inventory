"""
Validation utilities for input validation and data sanitization.
"""
import re
from typing import Any, Optional
from pydantic import EmailStr, ValidationError as PydanticValidationError


def validate_email_format(email: str) -> bool:
    """
    Validate email format using Pydantic EmailStr validation.
    
    Args:
        email: Email string to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    try:
        EmailStr.validate(email)
        return True
    except (PydanticValidationError, ValueError):
        return False


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format (10-14 digits only).
    
    Args:
        phone: Phone number string to validate
        
    Returns:
        bool: True if phone number is valid, False otherwise
    """
    if not phone:
        return False
    
    # Remove any non-digit characters for validation
    digits_only = re.sub(r'\D', '', phone)
    
    # Check if it contains only digits and is between 10-14 characters
    return len(digits_only) >= 10 and len(digits_only) <= 14 and digits_only.isdigit()


def validate_password_strength(password: str) -> tuple[bool, list[str]]:
    """
    Validate password meets complexity requirements.
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter  
    - At least one number
    - At least one special character
    
    Args:
        password: Password string to validate
        
    Returns:
        tuple: (is_valid: bool, errors: list[str])
    """
    errors = []
    
    if len(password) < 8:
        errors.append('Password must be at least 8 characters long')
    
    if not re.search(r'[A-Z]', password):
        errors.append('Password must contain at least one uppercase letter')
    
    if not re.search(r'[a-z]', password):
        errors.append('Password must contain at least one lowercase letter')
    
    if not re.search(r'\d', password):
        errors.append('Password must contain at least one number')
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append('Password must contain at least one special character')
    
    return len(errors) == 0, errors


def sanitize_string_input(value: Any, max_length: Optional[int] = None) -> str:
    """
    Sanitize string input by removing dangerous characters and trimming whitespace.
    
    Args:
        value: Input value to sanitize
        max_length: Optional maximum length to truncate to
        
    Returns:
        str: Sanitized string
    """
    if value is None:
        return ""
    
    # Convert to string and strip whitespace
    sanitized = str(value).strip()
    
    # Remove null bytes and other control characters
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', sanitized)
    
    # Truncate if max_length specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def validate_uuid_format(uuid_string: str) -> bool:
    """
    Validate UUID format.
    
    Args:
        uuid_string: UUID string to validate
        
    Returns:
        bool: True if UUID format is valid, False otherwise
    """
    if not uuid_string:
        return False
    
    # UUID v4 pattern
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
        re.IGNORECASE
    )
    
    return bool(uuid_pattern.match(uuid_string))


def validate_positive_integer(value: Any) -> bool:
    """
    Validate that a value is a positive integer.
    
    Args:
        value: Value to validate
        
    Returns:
        bool: True if value is a positive integer, False otherwise
    """
    try:
        int_value = int(value)
        return int_value > 0
    except (ValueError, TypeError):
        return False


def validate_non_negative_integer(value: Any) -> bool:
    """
    Validate that a value is a non-negative integer (>= 0).
    
    Args:
        value: Value to validate
        
    Returns:
        bool: True if value is a non-negative integer, False otherwise
    """
    try:
        int_value = int(value)
        return int_value >= 0
    except (ValueError, TypeError):
        return False


def validate_string_length(value: str, min_length: int = 0, max_length: Optional[int] = None) -> bool:
    """
    Validate string length constraints.
    
    Args:
        value: String to validate
        min_length: Minimum required length
        max_length: Maximum allowed length (optional)
        
    Returns:
        bool: True if string meets length requirements, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    if len(value) < min_length:
        return False
    
    if max_length is not None and len(value) > max_length:
        return False
    
    return True


def validate_enum_value(value: str, valid_values: list[str]) -> bool:
    """
    Validate that a value is in a list of valid enum values.
    
    Args:
        value: Value to validate
        valid_values: List of valid enum values
        
    Returns:
        bool: True if value is valid, False otherwise
    """
    return value in valid_values


def sanitize_sql_input(value: str) -> str:
    """
    Basic SQL injection prevention by escaping single quotes.
    Note: This is a basic sanitization. Parameterized queries should be used primarily.
    
    Args:
        value: String value to sanitize
        
    Returns:
        str: Sanitized string with escaped quotes
    """
    if not isinstance(value, str):
        return str(value)
    
    # Escape single quotes by doubling them
    return value.replace("'", "''")