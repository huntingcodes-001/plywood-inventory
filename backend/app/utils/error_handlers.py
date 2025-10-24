"""
Error handling middleware and response formatting for FastAPI.
"""
from typing import Any, Dict, Optional
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError as PydanticValidationError
import logging

from .exceptions import (
    InventoryManagementException,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    DatabaseError,
    BusinessLogicError,
    ResourceNotFoundError,
    ResourceConflictError,
    InvalidCredentialsError,
    TokenExpiredError,
    InvalidTokenError,
    UnauthorizedRoleError,
    UserNotActiveError,
    EmailNotInvitedError,
    DuplicateEmailError,
    InsufficientStockError
)

# Configure logger
logger = logging.getLogger(__name__)


class ErrorResponse(BaseModel):
    """Standard error response format."""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None


def create_error_response(
    error_type: str,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    status_code: int = 500
) -> JSONResponse:
    """
    Create a standardized error response.
    
    Args:
        error_type: Type of error (e.g., "AUTHENTICATION_ERROR")
        message: Human-readable error message
        details: Optional additional error details
        status_code: HTTP status code
        
    Returns:
        JSONResponse: Formatted error response
    """
    error_response = ErrorResponse(
        error=error_type,
        message=message,
        details=details
    )
    
    return JSONResponse(
        status_code=status_code,
        content=error_response.dict(exclude_none=True)
    )


async def authentication_error_handler(request: Request, exc: AuthenticationError) -> JSONResponse:
    """Handle authentication errors."""
    logger.warning(f"Authentication error: {exc.message}")
    
    # Map specific authentication errors to appropriate status codes
    if isinstance(exc, (InvalidCredentialsError, UserNotActiveError)):
        status_code = 401
        error_type = "AUTHENTICATION_ERROR"
    elif isinstance(exc, (TokenExpiredError, InvalidTokenError)):
        status_code = 401
        error_type = "TOKEN_ERROR"
    else:
        status_code = 401
        error_type = "AUTHENTICATION_ERROR"
    
    return create_error_response(
        error_type=error_type,
        message=exc.message,
        details=exc.details,
        status_code=status_code
    )


async def authorization_error_handler(request: Request, exc: AuthorizationError) -> JSONResponse:
    """Handle authorization errors."""
    logger.warning(f"Authorization error: {exc.message}")
    
    # Map specific authorization errors
    if isinstance(exc, UnauthorizedRoleError):
        error_type = "INSUFFICIENT_PERMISSIONS"
    elif isinstance(exc, EmailNotInvitedError):
        error_type = "EMAIL_NOT_INVITED"
    else:
        error_type = "AUTHORIZATION_ERROR"
    
    return create_error_response(
        error_type=error_type,
        message=exc.message,
        details=exc.details,
        status_code=403
    )


async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle validation errors."""
    logger.info(f"Validation error: {exc.message}")
    
    return create_error_response(
        error_type="VALIDATION_ERROR",
        message=exc.message,
        details=exc.details,
        status_code=400
    )


async def database_error_handler(request: Request, exc: DatabaseError) -> JSONResponse:
    """Handle database errors."""
    logger.error(f"Database error: {exc.message}")
    
    return create_error_response(
        error_type="DATABASE_ERROR",
        message="A database error occurred. Please try again later.",
        status_code=500
    )


async def business_logic_error_handler(request: Request, exc: BusinessLogicError) -> JSONResponse:
    """Handle business logic errors."""
    logger.info(f"Business logic error: {exc.message}")
    
    # Map specific business logic errors
    if isinstance(exc, InsufficientStockError):
        error_type = "INSUFFICIENT_STOCK"
        status_code = 400
    else:
        error_type = "BUSINESS_LOGIC_ERROR"
        status_code = 400
    
    return create_error_response(
        error_type=error_type,
        message=exc.message,
        details=exc.details,
        status_code=status_code
    )


async def resource_not_found_error_handler(request: Request, exc: ResourceNotFoundError) -> JSONResponse:
    """Handle resource not found errors."""
    logger.info(f"Resource not found: {exc.message}")
    
    return create_error_response(
        error_type="RESOURCE_NOT_FOUND",
        message=exc.message,
        details=exc.details,
        status_code=404
    )


async def resource_conflict_error_handler(request: Request, exc: ResourceConflictError) -> JSONResponse:
    """Handle resource conflict errors."""
    logger.info(f"Resource conflict: {exc.message}")
    
    # Map specific conflict errors
    if isinstance(exc, DuplicateEmailError):
        error_type = "DUPLICATE_EMAIL"
    else:
        error_type = "RESOURCE_CONFLICT"
    
    return create_error_response(
        error_type=error_type,
        message=exc.message,
        details=exc.details,
        status_code=409
    )


async def request_validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle FastAPI request validation errors."""
    logger.info(f"Request validation error: {exc.errors()}")
    
    # Format validation errors for better readability
    formatted_errors = []
    for error in exc.errors():
        field_path = " -> ".join(str(loc) for loc in error["loc"])
        formatted_errors.append({
            "field": field_path,
            "message": error["msg"],
            "type": error["type"]
        })
    
    return create_error_response(
        error_type="REQUEST_VALIDATION_ERROR",
        message="Request validation failed",
        details={"validation_errors": formatted_errors},
        status_code=422
    )


async def pydantic_validation_error_handler(request: Request, exc: PydanticValidationError) -> JSONResponse:
    """Handle Pydantic validation errors."""
    logger.info(f"Pydantic validation error: {exc.errors()}")
    
    # Format validation errors
    formatted_errors = []
    for error in exc.errors():
        field_path = " -> ".join(str(loc) for loc in error["loc"])
        formatted_errors.append({
            "field": field_path,
            "message": error["msg"],
            "type": error["type"]
        })
    
    return create_error_response(
        error_type="VALIDATION_ERROR",
        message="Data validation failed",
        details={"validation_errors": formatted_errors},
        status_code=422
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTP exceptions."""
    logger.info(f"HTTP exception: {exc.status_code} - {exc.detail}")
    
    return create_error_response(
        error_type="HTTP_ERROR",
        message=exc.detail,
        status_code=exc.status_code
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    
    return create_error_response(
        error_type="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred. Please try again later.",
        status_code=500
    )


def register_exception_handlers(app):
    """
    Register all exception handlers with the FastAPI app.
    
    Args:
        app: FastAPI application instance
    """
    # Custom exception handlers
    app.add_exception_handler(AuthenticationError, authentication_error_handler)
    app.add_exception_handler(AuthorizationError, authorization_error_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(DatabaseError, database_error_handler)
    app.add_exception_handler(BusinessLogicError, business_logic_error_handler)
    app.add_exception_handler(ResourceNotFoundError, resource_not_found_error_handler)
    app.add_exception_handler(ResourceConflictError, resource_conflict_error_handler)
    
    # FastAPI built-in exception handlers
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(PydanticValidationError, pydantic_validation_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    
    # Catch-all exception handler
    app.add_exception_handler(Exception, general_exception_handler)