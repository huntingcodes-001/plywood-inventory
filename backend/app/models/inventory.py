from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class InventoryItemCreate(BaseModel):
    """Model for creating new inventory items"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    stock_level: int = Field(..., ge=0)
    low_stock_threshold: int = Field(..., ge=0)

    class Config:
        from_attributes = True


class InventoryItemUpdate(BaseModel):
    """Model for updating existing inventory items"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    stock_level: Optional[int] = Field(None, ge=0)
    low_stock_threshold: Optional[int] = Field(None, ge=0)

    class Config:
        from_attributes = True


class InventoryItemResponse(BaseModel):
    """Model for inventory item responses"""
    id: str
    name: str
    description: Optional[str] = None
    stock_level: int
    low_stock_threshold: int
    created_at: datetime
    updated_at: datetime

    @property
    def is_low_stock(self) -> bool:
        """Check if item is below low stock threshold"""
        return self.stock_level <= self.low_stock_threshold

    class Config:
        from_attributes = True