"""
JWT token creation, validation, and decoding utilities.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from ..config import settings


class JWTError(Exception):
    """Custom exception for JWT-related errors."""
    pass


def create_access_token(user_id: str, role: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with user_id and role claims.
    
    Args:
        user_id: User's unique identifier
        role: User's role (admin, salesperson, warehouse_manager)
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token as string
        
    Raises:
        JWTError: If token creation fails
    """
    try:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)
        
        payload = {
            "user_id": user_id,
            "role": role,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        token = jwt.encode(
            payload, 
            settings.jwt_secret_key, 
            algorithm=settings.jwt_algorithm
        )
        
        return token
    except Exception as e:
        raise JWTError(f"Failed to create access token: {str(e)}")


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT access token.
    
    Args:
        token: JWT token to decode
        
    Returns:
        Dictionary containing token payload
        
    Raises:
        JWTError: If token is invalid, expired, or malformed
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        
        # Validate token type
        if payload.get("type") != "access":
            raise JWTError("Invalid token type")
        
        # Validate required claims
        if not payload.get("user_id") or not payload.get("role"):
            raise JWTError("Missing required claims in token")
        
        return payload
        
    except ExpiredSignatureError:
        raise JWTError("Token has expired")
    except InvalidTokenError as e:
        raise JWTError(f"Invalid token: {str(e)}")
    except Exception as e:
        raise JWTError(f"Token decode error: {str(e)}")


def validate_token(token: str) -> bool:
    """
    Validate if a JWT token is valid without decoding.
    
    Args:
        token: JWT token to validate
        
    Returns:
        True if token is valid, False otherwise
    """
    try:
        decode_access_token(token)
        return True
    except JWTError:
        return False


def extract_user_info(token: str) -> tuple[str, str]:
    """
    Extract user_id and role from JWT token.
    
    Args:
        token: JWT token to extract info from
        
    Returns:
        Tuple of (user_id, role)
        
    Raises:
        JWTError: If token is invalid or missing required claims
    """
    payload = decode_access_token(token)
    user_id = payload.get("user_id")
    role = payload.get("role")
    
    if not user_id or not role:
        raise JWTError("Missing user information in token")
    
    return user_id, role


def get_token_expiration(token: str) -> Optional[datetime]:
    """
    Get the expiration time of a JWT token.
    
    Args:
        token: JWT token to check
        
    Returns:
        Expiration datetime or None if token is invalid
    """
    try:
        payload = decode_access_token(token)
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            return datetime.fromtimestamp(exp_timestamp)
        return None
    except JWTError:
        return None


def is_token_expired(token: str) -> bool:
    """
    Check if a JWT token is expired.
    
    Args:
        token: JWT token to check
        
    Returns:
        True if token is expired, False otherwise
    """
    try:
        decode_access_token(token)
        return False
    except JWTError as e:
        return "expired" in str(e).lower()