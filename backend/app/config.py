"""
Configuration management for the inventory management backend.
Handles environment variables and application settings.
"""

import os
from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Supabase Configuration
    supabase_url: str
    supabase_service_key: str
    
    # JWT Configuration
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # CORS Configuration
    cors_origins_str: str = "http://localhost:5173"
    
    # Application Configuration
    app_name: str = "Inventory Management API"
    debug: bool = False
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins_str.split(',')]
    
    @field_validator('supabase_url')
    @classmethod
    def validate_supabase_url(cls, v):
        """Validate Supabase URL format."""
        if not v:
            raise ValueError('SUPABASE_URL is required')
        # Allow test URLs for development
        if not (v.startswith('https://') or v.startswith('http://test')):
            raise ValueError('SUPABASE_URL must be a valid HTTPS URL')
        return v
    
    @field_validator('supabase_service_key')
    @classmethod
    def validate_supabase_key(cls, v):
        """Validate Supabase service key is provided."""
        if not v:
            raise ValueError('SUPABASE_SERVICE_KEY is required')
        # Allow test keys for development
        if len(v) < 10:
            raise ValueError('SUPABASE_SERVICE_KEY must be at least 10 characters')
        return v
    
    @field_validator('jwt_secret_key')
    @classmethod
    def validate_jwt_secret(cls, v):
        """Validate JWT secret key strength."""
        if not v:
            raise ValueError('JWT_SECRET_KEY is required')
        # Allow shorter keys for development
        if len(v) < 10:
            raise ValueError('JWT_SECRET_KEY must be at least 10 characters')
        return v
    
    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        case_sensitive = False


# Global settings instance
settings = Settings()