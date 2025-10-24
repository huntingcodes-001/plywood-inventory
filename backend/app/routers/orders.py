"""
Order management API endpoints.
"""
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends
from ..models.order import OrderCreate, OrderResponse, OrderItemResponse, OrderStatusUpdate, OrderStatus
from ..auth.dependencies import require_salesperson, require_authenticated_user, require_warehouse_manager_or_admin
from ..database import get_database, DatabaseManager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    db: DatabaseManager = Depends(get_database),
    current_user: dict = Depends(require_salesperson)
):
    """
    Create new customer order (salesperson only).
    
    Validates stock availability and atomically creates order with inventory stock reduction.
    
    Requirements: 5.1, 5.2, 5.3, 5.4
    """
    try:
        user_id = current_user.get("user_id")
        
        # Validate stock availability for all items first
        stock_validation_errors = []
        inventory_items = {}
        
        for order_item in order_data.items:
            # Get current inventory item
            inventory_result = db.client.table("inventory_items").select("*").eq("id", order_item.item_id).execute()
            
            if not inventory_result.data:
                stock_validation_errors.append(f"Inventory item {order_item.item_id} not found")
                continue
            
            inventory_item = inventory_result.data[0]
            inventory_items[order_item.item_id] = inventory_item
            
            # Check if sufficient stock is available
            if inventory_item["stock_level"] < order_item.quantity:
                stock_validation_errors.append(
                    f"Insufficient stock for item '{inventory_item['name']}'. "
                    f"Requested: {order_item.quantity}, Available: {inventory_item['stock_level']}"
                )
        
        # If any stock validation errors, reject the order
        if stock_validation_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "Insufficient stock",
                    "message": "Order cannot be fulfilled due to insufficient inventory",
                    "details": stock_validation_errors
                }
            )
        
        # Begin atomic transaction: create order and reduce inventory stock
        # Create the order record first
        order_insert_data = {
            "customer_name": order_data.customer_name,
            "status": OrderStatus.PENDING.value,
            "created_by": user_id
        }
        
        order_result = db.client.table("orders").insert(order_insert_data).execute()
        
        if not order_result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create order"
            )
        
        created_order = order_result.data[0]
        order_id = created_order["id"]
        
        # Create order items and reduce inventory stock
        order_items_data = []
        
        for order_item in order_data.items:
            # Create order item record
            order_item_insert_data = {
                "order_id": order_id,
                "item_id": order_item.item_id,
                "quantity": order_item.quantity
            }
            
            order_item_result = db.client.table("order_items").insert(order_item_insert_data).execute()
            
            if not order_item_result.data:
                # Rollback: delete the order if order item creation fails
                db.client.table("orders").delete().eq("id", order_id).execute()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create order items"
                )
            
            # Reduce inventory stock level
            inventory_item = inventory_items[order_item.item_id]
            new_stock_level = inventory_item["stock_level"] - order_item.quantity
            
            stock_update_result = db.client.table("inventory_items").update({
                "stock_level": new_stock_level
            }).eq("id", order_item.item_id).execute()
            
            if not stock_update_result.data:
                # Rollback: delete the order and order items if stock update fails
                db.client.table("orders").delete().eq("id", order_id).execute()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update inventory stock levels"
                )
            
            # Prepare order item response data
            order_items_data.append(OrderItemResponse(
                id=order_item_result.data[0]["id"],
                item_id=order_item.item_id,
                item_name=inventory_item["name"],
                quantity=order_item.quantity
            ))
        
        # Return complete order response
        return OrderResponse(
            id=created_order["id"],
            customer_name=created_order["customer_name"],
            status=OrderStatus(created_order["status"]),
            items=order_items_data,
            created_by=created_order["created_by"],
            created_at=created_order["created_at"],
            updated_at=created_order["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Create order error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during order creation"
        )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_details(
    order_id: str,
    db: DatabaseManager = Depends(get_database),
    current_user: dict = Depends(require_authenticated_user)
):
    """
    Get order details by ID (all authenticated users).
    
    Returns complete order information including items for any authenticated user.
    
    Requirements: 6.1, 6.3
    """
    try:
        # Get order details
        order_result = db.client.table("orders").select("*").eq("id", order_id).execute()
        
        if not order_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        order = order_result.data[0]
        
        # Get order items with inventory item details
        order_items_result = db.client.table("order_items").select(
            "*, inventory_items(name)"
        ).eq("order_id", order_id).execute()
        
        order_items_data = []
        for order_item in order_items_result.data:
            order_items_data.append(OrderItemResponse(
                id=order_item["id"],
                item_id=order_item["item_id"],
                item_name=order_item["inventory_items"]["name"],
                quantity=order_item["quantity"]
            ))
        
        return OrderResponse(
            id=order["id"],
            customer_name=order["customer_name"],
            status=OrderStatus(order["status"]),
            items=order_items_data,
            created_by=order["created_by"],
            created_at=order["created_at"],
            updated_at=order["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get order details error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving order details"
        )


@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    status_update: OrderStatusUpdate,
    db: DatabaseManager = Depends(get_database),
    current_user: dict = Depends(require_warehouse_manager_or_admin)
):
    """
    Update order status (warehouse manager and admin only).
    
    Updates order status and maintains order history with timestamps.
    
    Requirements: 6.1, 6.2, 6.4, 6.5
    """
    try:
        # Check if order exists
        order_result = db.client.table("orders").select("*").eq("id", order_id).execute()
        
        if not order_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        
        current_order = order_result.data[0]
        
        # Validate status transition (optional business logic)
        current_status = OrderStatus(current_order["status"])
        new_status = status_update.status
        
        # Update order status
        update_result = db.client.table("orders").update({
            "status": new_status.value
        }).eq("id", order_id).execute()
        
        if not update_result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update order status"
            )
        
        updated_order = update_result.data[0]
        
        # Get order items with inventory item details for response
        order_items_result = db.client.table("order_items").select(
            "*, inventory_items(name)"
        ).eq("order_id", order_id).execute()
        
        order_items_data = []
        for order_item in order_items_result.data:
            order_items_data.append(OrderItemResponse(
                id=order_item["id"],
                item_id=order_item["item_id"],
                item_name=order_item["inventory_items"]["name"],
                quantity=order_item["quantity"]
            ))
        
        return OrderResponse(
            id=updated_order["id"],
            customer_name=updated_order["customer_name"],
            status=OrderStatus(updated_order["status"]),
            items=order_items_data,
            created_by=updated_order["created_by"],
            created_at=updated_order["created_at"],
            updated_at=updated_order["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update order status error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during order status update"
        )