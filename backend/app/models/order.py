from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    FULFILLED = "fulfilled"


class OrderItemCreate(BaseModel):
    """Model for creating order items"""
    item_id: str
    quantity: int = Field(..., gt=0)

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Model for creating new orders"""
    customer_name: str = Field(..., min_length=1, max_length=255)
    items: List[OrderItemCreate] = Field(..., min_items=1)

    class Config:
        from_attributes = True


class OrderItemResponse(BaseModel):
    """Model for order item responses"""
    id: str
    item_id: str
    item_name: str
    quantity: int

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Model for order responses"""
    id: str
    customer_name: str
    status: OrderStatus
    items: List[OrderItemResponse]
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        use_enum_values = True
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    """Model for updating order status"""
    status: OrderStatus

    class Config:
        use_enum_values = True