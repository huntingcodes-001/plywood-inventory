"""
Inventory management API endpoints.
"""
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from ..models.inventory import InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse
from ..auth.dependencies import require_authenticated_user, require_warehouse_manager_or_admin
from ..database import get_database, DatabaseManager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("", response_model=List[InventoryItemResponse])
async def list_inventory_items(
    db: DatabaseManager = Depends(get_database),
    current_user: dict = Depends(require_authenticated_user)
):
    """
    List all inventory items with stock levels and threshold information.
    
    Available to all authenticated users regardless of role.
    
    Requirements: 4.1
    """
    try:
        # Get all inventory items
        result = db.client.table("inventory_items").select("*").execute()
        
        items = []
        for item_data in result.data:
            items.append(InventoryItemResponse(
                id=item_data["id"],
                name=item_data["name"],
                description=item_data.get("description"),
                stock_level=item_data["stock_level"],
                low_stock_threshold=item_data["low_stock_threshold"],
                created_at=item_data["created_at"],
                updated_at=item_data["updated_at"]
            ))
        
        return items
        
    except Exception as e:
        logger.error(f"List inventory items error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving inventory items"
        )


@router.post("", response_model=InventoryItemResponse)
async def create_inventory_item(
    item_data: InventoryItemCreate,
    db: DatabaseManager = Depends(get_database),
    current_user: dict = Depends(require_warehouse_manager_or_admin)
):
    """
    Create new inventory item (admin and warehouse manager only).
    
    Creates a new inventory item with the provided details.
    
    Requirements: 4.2
    """
    try:
        # Check if item with this name already exists
        existing_item_result = db.client.table("inventory_items").select("*").eq("name", item_data.name).execute()
        
        if existing_item_result.data:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Inventory item with this name already exists"
            )
        
        # Create inventory item record
        insert_data = {
            "name": item_data.name,
            "description": item_data.description,
            "stock_level": item_data.stock_level,
            "low_stock_threshold": item_data.low_stock_threshold
        }
        
        result = db.client.table("inventory_items").insert(insert_data).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create inventory item"
            )
        
        created_item = result.data[0]
        
        # Return inventory item response
        return InventoryItemResponse(
            id=created_item["id"],
            name=created_item["name"],
            description=created_item.get("description"),
            stock_level=created_item["stock_level"],
            low_stock_threshold=created_item["low_stock_threshold"],
            created_at=created_item["created_at"],
            updated_at=created_item["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create inventory item error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during inventory item creation"
        )


@router.put("/{item_id}", response_model=InventoryItemResponse)
async def update_inventory_item(
    item_id: str,
    item_data: InventoryItemUpdate,
    db: DatabaseManager = Depends(get_database),
    current_user: dict = Depends(require_warehouse_manager_or_admin)
):
    """
    Update inventory item details and stock levels (admin and warehouse manager only).
    
    Updates existing inventory item with provided data. Only non-null fields are updated.
    
    Requirements: 4.3, 4.4
    """
    try:
        # Check if item exists
        existing_item_result = db.client.table("inventory_items").select("*").eq("id", item_id).execute()
        
        if not existing_item_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory item not found"
            )
        
        # Build update data with only provided fields
        update_data = {}
        if item_data.name is not None:
            # Check if another item with this name already exists
            name_check_result = db.client.table("inventory_items").select("*").eq("name", item_data.name).neq("id", item_id).execute()
            if name_check_result.data:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Another inventory item with this name already exists"
                )
            update_data["name"] = item_data.name
        
        if item_data.description is not None:
            update_data["description"] = item_data.description
        
        if item_data.stock_level is not None:
            update_data["stock_level"] = item_data.stock_level
        
        if item_data.low_stock_threshold is not None:
            update_data["low_stock_threshold"] = item_data.low_stock_threshold
        
        # If no fields to update, return current item
        if not update_data:
            existing_item = existing_item_result.data[0]
            return InventoryItemResponse(
                id=existing_item["id"],
                name=existing_item["name"],
                description=existing_item.get("description"),
                stock_level=existing_item["stock_level"],
                low_stock_threshold=existing_item["low_stock_threshold"],
                created_at=existing_item["created_at"],
                updated_at=existing_item["updated_at"]
            )
        
        # Update the item
        update_result = db.client.table("inventory_items").update(update_data).eq("id", item_id).execute()
        
        if not update_result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update inventory item"
            )
        
        updated_item = update_result.data[0]
        
        return InventoryItemResponse(
            id=updated_item["id"],
            name=updated_item["name"],
            description=updated_item.get("description"),
            stock_level=updated_item["stock_level"],
            low_stock_threshold=updated_item["low_stock_threshold"],
            created_at=updated_item["created_at"],
            updated_at=updated_item["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update inventory item error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during inventory item update"
        )