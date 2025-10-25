from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re


class UserRole(str, Enum):
    ADMIN = "admin"
    SALESPERSON = "salesperson"
    WAREHOUSE_MANAGER = "warehouse_manager"


class UserStatus(str, Enum):
    INVITED = "invited"
    ACTIVE = "active"


class UserCreate(BaseModel):
    """Model for creating user invitations (admin only)"""
    email: EmailStr
    role: UserRole

    class Config:
        use_enum_values = True


class UserRegister(BaseModel):
    """Model for user registration completion"""
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    # FIX: Changed 'regex' to 'pattern' for Pydantic V2 compatibility
    phone_number: str = Field(..., pattern=r'^\d{10,14}$')
    # FIX: Changed 'regex' to 'pattern' for Pydantic V2 compatibility
    emergency_contact_number: str = Field(..., pattern=r'^\d{10,14}$')
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password_complexity(cls, v):
        """Validate password meets complexity requirements"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        
        return v

    class Config:
        use_enum_values = True


class UserResponse(BaseModel):
    """Model for user data responses"""
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    emergency_contact_number: Optional[str] = None
    role: UserRole
    status: UserStatus
    created_at: datetime

    class Config:
        use_enum_values = True
        from_attributes = True


class LoginRequest(BaseModel):
    """Model for login requests"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Model for login responses"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse