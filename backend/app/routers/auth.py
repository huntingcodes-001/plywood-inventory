"""
Authentication API endpoints for login and user registration.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from ..models.user import LoginRequest, LoginResponse, UserRegister, UserResponse
from ..auth.password import verify_password, hash_password
from ..auth.jwt_handler import create_access_token
from ..database import get_database, DatabaseManager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: DatabaseManager = Depends(get_database)
):
    """
    Authenticate user with email and password credentials.
    
    Returns JWT token with user information on successful authentication.
    
    Requirements: 1.1, 1.2
    """
    try:
        # Query user by email
        result = db.client.table("users").select("*").eq("email", login_data.email).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        user_data = result.data[0]
        
        # Check if user is active
        if user_data.get("status") != "active":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is not active. Please complete registration first."
            )
        
        # Verify password
        if not user_data.get("password_hash"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not verify_password(login_data.password, user_data["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Create JWT token
        access_token = create_access_token(
            user_id=user_data["id"],
            role=user_data["role"]
        )
        
        # Create user response object
        user_response = UserResponse(
            id=user_data["id"],
            email=user_data["email"],
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            phone_number=user_data.get("phone_number"),
            emergency_contact_number=user_data.get("emergency_contact_number"),
            role=user_data["role"],
            status=user_data["status"],
            created_at=user_data["created_at"]
        )
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication"
        )


@router.post("/register", response_model=UserResponse)
async def register(
    registration_data: UserRegister,
    db: DatabaseManager = Depends(get_database)
):
    """
    Complete user registration for invited users.
    
    Verifies email invitation exists and updates user record with registration details.
    
    Requirements: 3.1, 3.2, 3.3
    """
    try:
        # Check if user exists with invited status
        result = db.client.table("users").select("*").eq("email", registration_data.email).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This email is not authorized to register"
            )
        
        user_data = result.data[0]
        
        # Verify user has invited status
        if user_data.get("status") != "invited":
            if user_data.get("status") == "active":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="User is already registered and active"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="This email is not authorized to register"
                )
        
        # Hash the password
        password_hash = hash_password(registration_data.password)
        
        # Update user record with registration details
        update_data = {
            "first_name": registration_data.first_name,
            "last_name": registration_data.last_name,
            "phone_number": registration_data.phone_number,
            "emergency_contact_number": registration_data.emergency_contact_number,
            "password_hash": password_hash,
            "status": "active",
            "updated_at": "now()"
        }
        
        update_result = db.client.table("users").update(update_data).eq("id", user_data["id"]).execute()
        
        if not update_result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to complete registration"
            )
        
        updated_user = update_result.data[0]
        
        # Return user response
        return UserResponse(
            id=updated_user["id"],
            email=updated_user["email"],
            first_name=updated_user["first_name"],
            last_name=updated_user["last_name"],
            phone_number=updated_user["phone_number"],
            emergency_contact_number=updated_user["emergency_contact_number"],
            role=updated_user["role"],
            status=updated_user["status"],
            created_at=updated_user["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )