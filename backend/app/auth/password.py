"""
Password hashing and validation utilities using bcrypt.
"""
import re
from typing import Optional
import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with salt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password as string
    """
    # Generate salt and hash password
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        password: Plain text password to verify
        hashed_password: Stored hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False


def validate_password_complexity(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password meets complexity requirements.
    
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter  
    - At least one number
    - At least one special character
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, None


def is_password_valid(password: str) -> bool:
    """
    Check if password meets complexity requirements.
    
    Args:
        password: Password to validate
        
    Returns:
        True if password is valid, False otherwise
    """
    is_valid, _ = validate_password_complexity(password)
    return is_valid