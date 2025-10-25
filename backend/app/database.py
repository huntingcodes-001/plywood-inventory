"""
Database connection and utilities for Supabase PostgreSQL.
Handles Supabase client initialization and connection management.
"""

# FIX: Changed import path to avoid conflicting internal imports from the 'realtime' package.
from supabase.client import create_client, Client 
from .config import settings
import logging
from typing import Optional, Dict, Any
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)


class DatabaseConnectionError(Exception):
    """Custom exception for database connection errors."""
    pass


class DatabaseManager:
    """Manages Supabase database connections and operations."""
    
    def __init__(self):
        self._client: Optional[Client] = None
        self._connection_healthy: bool = False
        self._last_health_check: Optional[datetime] = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Supabase client with configuration."""
        try:
            self._client = create_client(
                settings.supabase_url,
                settings.supabase_service_key
            )
            logger.info("Supabase client initialized successfully")
            
            # Perform initial health check
            if self._perform_sync_health_check():
                self._connection_healthy = True
                logger.info("Database connection verified")
            else:
                logger.warning("Database connection could not be verified during initialization")
                
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            # In development, don't crash the app - just mark as unhealthy
            if settings.debug:
                logger.warning("Running in debug mode - continuing without database connection")
                self._connection_healthy = False
                self._client = None
            else:
                raise DatabaseConnectionError(f"Failed to initialize database connection: {e}")
    
    @property
    def client(self) -> Client:
        """Get the Supabase client instance."""
        if not self._client:
            self._initialize_client()
        if not self._client:
            raise DatabaseConnectionError("Database client is not available")
        return self._client
    
    def _perform_sync_health_check(self) -> bool:
        """
        Perform synchronous health check for initialization.
        
        Returns:
            bool: True if connection is healthy, False otherwise
        """
        try:
            # FIX: Added params={} to satisfy new library requirements
            result = self._client.rpc('version', params={}).execute()
            return result is not None
        except Exception as e:
            logger.error(f"Sync health check failed: {e}")
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a comprehensive health check on the database connection.
        
        Returns:
            Dict containing health check results and metadata
        """
        health_status = {
            "healthy": False,
            "timestamp": datetime.utcnow().isoformat(),
            "connection_status": "unknown",
            "error": None
        }
        
        try:
            if not self._client:
                health_status["connection_status"] = "no_client"
                health_status["error"] = "Database client not initialized"
                return health_status
                
            # Test basic connection
            # FIX: Added params={} to satisfy new library requirements
            result = self._client.rpc('version', params={}).execute()
            
            if result:
                health_status["healthy"] = True
                health_status["connection_status"] = "connected"
                self._connection_healthy = True
                self._last_health_check = datetime.utcnow()
                logger.debug("Database health check passed")
            else:
                health_status["connection_status"] = "no_response"
                self._connection_healthy = False
                
        except Exception as e:
            health_status["error"] = str(e)
            health_status["connection_status"] = "error"
            self._connection_healthy = False
            logger.error(f"Database health check failed: {e}")
        
        return health_status
    
    def is_healthy(self) -> bool:
        """
        Check if the database connection is currently healthy.
        
        Returns:
            bool: True if connection is healthy, False otherwise
        """
        return self._connection_healthy
    
    def get_table(self, table_name: str):
        """
        Get a table reference for database operations.
        
        Args:
            table_name (str): Name of the table
            
        Returns:
            Supabase table reference
            
        Raises:
            DatabaseConnectionError: If database connection is not healthy
        """
        if not self._connection_healthy:
            raise DatabaseConnectionError("Database connection is not healthy")
            
        return self._client.table(table_name)
    
    def execute_query(self, query_func, *args, **kwargs):
        """
        Execute a database query with error handling.
        
        Args:
            query_func: Function to execute the query
            *args: Arguments for the query function
            **kwargs: Keyword arguments for the query function
            
        Returns:
            Query result
            
        Raises:
            DatabaseConnectionError: If query execution fails
        """
        try:
            result = query_func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Database query execution failed: {e}")
            # Mark connection as unhealthy if query fails
            self._connection_healthy = False
            raise DatabaseConnectionError(f"Query execution failed: {e}")
    
    def reconnect(self):
        """
        Attempt to reconnect to the database.
        
        Raises:
            DatabaseConnectionError: If reconnection fails
        """
        logger.info("Attempting to reconnect to database")
        try:
            self._client = None
            self._connection_healthy = False
            self._initialize_client()
            logger.info("Database reconnection successful")
        except Exception as e:
            logger.error(f"Database reconnection failed: {e}")
            raise DatabaseConnectionError(f"Reconnection failed: {e}")


# Global database manager instance
db_manager = DatabaseManager()


def get_database() -> DatabaseManager:
    """
    Dependency function to get database manager instance.
    
    Returns:
        DatabaseManager: The global database manager instance
    """
    return db_manager