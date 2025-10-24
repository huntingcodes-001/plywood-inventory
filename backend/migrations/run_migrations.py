#!/usr/bin/env python3
"""
Migration runner script for inventory management system.
Executes SQL migration files and database seeding.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from app.database import db_manager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def execute_sql_file(file_path: str) -> bool:
    """
    Execute a SQL file against the database.
    
    Args:
        file_path (str): Path to the SQL file
        
    Returns:
        bool: True if execution was successful, False otherwise
    """
    try:
        with open(file_path, 'r') as file:
            sql_content = file.read()
        
        # Split SQL content by statements (basic splitting on semicolons)
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement:
                # Execute each statement
                result = db_manager.client.rpc('exec_sql', {'sql': statement}).execute()
                
        logger.info(f"Successfully executed SQL file: {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error executing SQL file {file_path}: {e}")
        return False


def run_migrations():
    """
    Run all migration files in order.
    """
    logger.info("Starting database migrations...")
    
    try:
        # Check database connection
        if not db_manager.is_healthy():
            logger.error("Database connection is not healthy")
            return False
        
        migrations_dir = Path(__file__).parent
        
        # List of migration files in order
        migration_files = [
            "001_create_tables.sql",
            "002_seed_data.sql"
        ]
        
        # Execute each migration file
        for migration_file in migration_files:
            file_path = migrations_dir / migration_file
            
            if file_path.exists():
                logger.info(f"Executing migration: {migration_file}")
                
                if not execute_sql_file(str(file_path)):
                    logger.error(f"Migration failed: {migration_file}")
                    return False
            else:
                logger.warning(f"Migration file not found: {migration_file}")
        
        logger.info("All migrations completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Migration process failed: {e}")
        return False


def run_python_seeding():
    """
    Run Python-based seeding script.
    """
    logger.info("Running Python seeding script...")
    
    try:
        from seed_database import seed_database
        return seed_database()
    except Exception as e:
        logger.error(f"Python seeding failed: {e}")
        return False


if __name__ == "__main__":
    """
    Run migrations and seeding.
    """
    logger.info("🚀 Starting database setup process...")
    
    # Run SQL migrations
    if not run_migrations():
        logger.error("❌ SQL migrations failed")
        sys.exit(1)
    
    # Run Python seeding
    if not run_python_seeding():
        logger.error("❌ Database seeding failed")
        sys.exit(1)
    
    logger.info("✅ Database setup completed successfully")
    logger.info("Default admin credentials:")
    logger.info("  Email: admin@admin.com")
    logger.info("  Password: admin123!")
    sys.exit(0)