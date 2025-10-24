"""
FastAPI application entry point for the inventory management system.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import db_manager
from .routers import auth, users, inventory, orders
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Backend API for inventory management system with role-based access control",
    version="1.0.0",
    debug=settings.debug
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(inventory.router)
app.include_router(orders.router)


@app.on_event("startup")
async def startup_event():
    """Application startup event handler."""
    logger.info("Starting inventory management API...")
    
    # Validate database connection
    health_result = await db_manager.health_check()
    if not health_result.get("healthy", False):
        logger.warning("Database connection check failed during startup")
        if health_result.get("error"):
            logger.error(f"Database error: {health_result['error']}")
    else:
        logger.info("Database connection validated successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event handler."""
    logger.info("Shutting down inventory management API...")


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring application status.
    
    Returns:
        dict: Application health status
    """
    db_health = await db_manager.health_check()
    db_healthy = db_health.get("healthy", False)
    
    return {
        "status": "healthy" if db_healthy else "degraded",
        "database": "connected" if db_healthy else "disconnected",
        "database_details": db_health,
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: API welcome message and information
    """
    return {
        "message": "Inventory Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }