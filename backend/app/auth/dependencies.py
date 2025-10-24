"""
Authentication dependencies for FastAPI route protection and role-based access control.
"""
from typing import Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decode_access_token, JWTError


# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Extract and validate current user from JWT token.
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        Dictionary containing user information (user_id, role, etc.)
        
    Raises:
        HTTPException: 401 if token is invalid or missing
    """
    try:
        token = credentials.credentials
        payload = decode_access_token(token)
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def require_admin(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Require admin role for access.
    
    Args:
        current_user: Current user information from JWT token
        
    Returns:
        User information if admin role
        
    Raises:
        HTTPException: 403 if user is not admin
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def require_warehouse_manager_or_admin(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Require warehouse manager or admin role for access.
    
    Args:
        current_user: Current user information from JWT token
        
    Returns:
        User information if warehouse manager or admin role
        
    Raises:
        HTTPException: 403 if user is not warehouse manager or admin
    """
    allowed_roles = ["warehouse_manager", "admin"]
    if current_user.get("role") not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Warehouse manager or admin access required"
        )
    return current_user


async def require_salesperson(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Require salesperson role for access.
    
    Args:
        current_user: Current user information from JWT token
        
    Returns:
        User information if salesperson role
        
    Raises:
        HTTPException: 403 if user is not salesperson
    """
    if current_user.get("role") != "salesperson":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Salesperson access required"
        )
    return current_user


async def require_salesperson_or_admin(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Require salesperson or admin role for access.
    
    Args:
        current_user: Current user information from JWT token
        
    Returns:
        User information if salesperson or admin role
        
    Raises:
        HTTPException: 403 if user is not salesperson or admin
    """
    allowed_roles = ["salesperson", "admin"]
    if current_user.get("role") not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Salesperson or admin access required"
        )
    return current_user


async def require_authenticated_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Require any authenticated user (any role).
    
    Args:
        current_user: Current user information from JWT token
        
    Returns:
        User information for any authenticated user
    """
    return current_user


def get_user_id(current_user: Dict[str, Any] = Depends(get_current_user)) -> str:
    """
    Extract user ID from current user information.
    
    Args:
        current_user: Current user information from JWT token
        
    Returns:
        User ID as string
    """
    return current_user.get("user_id")


def get_user_role(current_user: Dict[str, Any] = Depends(get_current_user)) -> str:
    """
    Extract user role from current user information.
    
    Args:
        current_user: Current user information from JWT token
        
    Returns:
        User role as string
    """
    return current_user.get("role")