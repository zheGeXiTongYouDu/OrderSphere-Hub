from pydantic import BaseModel
from typing import Optional, List


class MenuItemBase(BaseModel):
    name: str
    price: float
    category: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    region: Optional[str] = None


class MenuItemCreate(MenuItemBase):
    raw_key: str


class MenuItemRead(MenuItemBase):
    id: int
    raw_key: str

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    customer_name: Optional[str] = None
    items: List[OrderItemCreate]


class OrderItemRead(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    menu_item: MenuItemRead

    class Config:
        from_attributes = True


class OrderRead(BaseModel):
    id: int
    customer_name: Optional[str]
    status: str
    total_price: float
    items: List[OrderItemRead]

    class Config:
        from_attributes = True
