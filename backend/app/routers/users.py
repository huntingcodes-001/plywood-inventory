"""
User management API endpoints for admin operations.
"""
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from ..models.user import UserCreate, UserResponse
from ..auth.dependencies import require_admin
from ..database import get_database, DatabaseManager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["user_management"])


@router.post("/invite", response_model=UserResponse)
async def invite_user(
    user_data: UserCreate,
    db: DatabaseManager = Depends(get_database),
    current_user: dict = Depends(require_admin)
):
    """
    Create user invitation (admin only).
    
    Creates a new user record with 'invited' status that can later complete registration.
    
    Requirements: 2.1, 2.2, 2.5
    """
    try:
        # Check if user with this email already exists
        existing_user_result = db.client.table("users").select("*").eq("email", user_data.email).execute()
        
        if existing_user_result.data:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        
        # Validate role is either salesperson or warehouse_manager
        allowed_roles = ["salesperson", "warehouse_manager"]
        if user_data.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role must be either 'salesperson' or 'warehouse_manager'"
            )
        
        # Create invited user record
        insert_data = {
            "email": user_data.email,
            "role": user_data.role,
            "status": "invited"
        }
        
        result = db.client.table("users").insert(insert_data).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user invitation"
            )
        
        created_user = result.data[0]
        
        # Return user response
        return UserResponse(
            id=created_user["id"],
            email=created_user["email"],
            first_name=created_user.get("first_name"),
            last_name=created_user.get("last_name"),
            phone_number=created_user.get("phone_number"),
            emergency_contact_number=created_user.get("emergency_contact_number"),
            role=created_user["role"],
            status=created_user["status"],
            created_at=created_user["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User invitation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during user invitation"
        )


@router.get("", response_model=List[UserResponse])
async def list_users(
    db: DatabaseManager = Depends(get_database),
    current_user: dict = Depends(require_admin)
):
    """
    List all users with invited and active status (admin only).
    
    Returns all users in the system regardless of their status.
    
    Requirements: 2.3
    """
    try:
        # Get all users with invited and active status
        result = db.client.table("users").select("*").in_("status", ["invited", "active"]).execute()
        
        users = []
        for user_data in result.data:
            users.append(UserResponse(
                id=user_data["id"],
                email=user_data["email"],
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                phone_number=user_data.get("phone_number"),
                emergency_contact_number=user_data.get("emergency_contact_number"),
                role=user_data["role"],
                status=user_data["status"],
                created_at=user_data["created_at"]
            ))
        
        return users
        
    except Exception as e:
        logger.error(f"List users error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving users"
        )


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: DatabaseManager = Depends(get_database),
    current_user: dict = Depends(require_admin)
):
    """
    Delete user by ID (admin only).
    
    Removes user record from the database.
    
    Requirements: 2.4
    """
    try:
        # Check if user exists
        existing_user_result = db.client.table("users").select("*").eq("id", user_id).execute()
        
        if not existing_user_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Prevent admin from deleting themselves
        if user_id == current_user.get("user_id"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own account"
            )
        
        # Delete the user
        delete_result = db.client.table("users").delete().eq("id", user_id).execute()
        
        if not delete_result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete user"
            )
        
        return {"message": "User deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Delete user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during user deletion"
        )