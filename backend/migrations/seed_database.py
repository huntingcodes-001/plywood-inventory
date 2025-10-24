#!/usr/bin/env python3
"""
Database seeding script for inventory management system.
Creates default admin user with bcrypt hashed password.
Includes validation for existing data to prevent duplicate seeding.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from passlib.context import CryptContext
from app.database import db_manager
from app.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password (str): Plain text password
        hashed_password (str): Hashed password
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def check_admin_exists() -> bool:
    """
    Check if default admin user already exists.
    
    Returns:
        bool: True if admin exists, False otherwise
    """
    try:
        result = db_manager.client.table('users').select('id').eq('email', 'admin@admin.com').execute()
        return len(result.data) > 0
    except Exception as e:
        logger.error(f"Error checking for existing admin user: {e}")
        return False


def create_admin_user() -> bool:
    """
    Create the default admin user.
    
    Returns:
        bool: True if user was created successfully, False otherwise
    """
    try:
        # Hash the default password
        hashed_password = hash_password("admin123!")
        
        # Create admin user data
        admin_data = {
            "first_name": "System",
            "last_name": "Administrator", 
            "email": "admin@admin.com",
            "password_hash": hashed_password,
            "phone_number": "1234567890",
            "emergency_contact_number": "1234567890",
            "role": "admin",
            "status": "active"
        }
        
        # Insert admin user
        result = db_manager.client.table('users').insert(admin_data).execute()
        
        if result.data:
            logger.info("Default admin user created successfully")
            logger.info("Email: admin@admin.com")
            logger.info("Password: admin123!")
            return True
        else:
            logger.error("Failed to create admin user - no data returned")
            return False
            
    except Exception as e:
        logger.error(f"Error creating admin user: {e}")
        return False


def seed_database():
    """
    Main seeding function that creates default data.
    """
    logger.info("Starting database seeding process...")
    
    try:
        # Check database connection
        if not db_manager.is_healthy():
            logger.error("Database connection is not healthy")
            return False
        
        # Check if admin user already exists
        if check_admin_exists():
            logger.info("Default admin user already exists - skipping creation")
            return True
        
        # Create admin user
        if create_admin_user():
            logger.info("Database seeding completed successfully")
            return True
        else:
            logger.error("Database seeding failed")
            return False
            
    except Exception as e:
        logger.error(f"Database seeding failed with error: {e}")
        return False


if __name__ == "__main__":
    """
    Run the seeding script directly.
    """
    success = seed_database()
    
    if success:
        logger.info("✅ Database seeding completed successfully")
        sys.exit(0)
    else:
        logger.error("❌ Database seeding failed")
        sys.exit(1)