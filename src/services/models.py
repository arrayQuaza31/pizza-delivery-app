from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional


class NewUserModel(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    password: str
    is_staff: bool
    is_active: bool


class UserUpdateModel(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]


class NewOrderModel(BaseModel):
    id: uuid.UUID
    quantity: int
    order_status: str
    pizza_size: str
    user_id: str
    time_of_order: datetime
