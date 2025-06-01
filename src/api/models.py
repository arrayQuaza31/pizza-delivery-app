from pydantic import BaseModel
from typing import Optional

# ----- User Models ------

class SignUpModel(BaseModel):
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]
    class Config:
        from_attributes=True
        json_schema_extra = {
            'example': {
                'username': 'johndoe', 
                'email': 'johndoe@email.com', 
                'password': 'password', 
                'is_staff': False, 
                'is_active': True
            }
        }

class LoginModel(BaseModel):
    username: str
    password: str
    class Config:
        from_attributes=True
        json_schema_extra = {
            'example': {
                'username': '<your username>', 
                'password': '<your password>'
            }
        }

class UpdateModel(BaseModel):
    username: str
    email: Optional[str]
    password: Optional[str]
    class Config:
        from_attributes=True
        json_schema_extra = {
            'example': {
                'email': '<your email> - if you want to update your tagged email', 
                'password': '<your password> - if you want to update your account password'
            }
        }

class Settings(BaseModel):
    authjwt_secret_key: str = '93ba757a8da35f4e1f933fc00af060fb1d970f84ec70d66259ad6db5ae3d1486'

# -------------------------
# ----- Order Models ------

class PlaceOrderModel(BaseModel):
    quantity: int
    order_status: str
    pizza_size: str
    class Config:
        from_attributes=True
        json_schema_extra = {
            'example': {
                'quantity': 1, 
                'order_status': 'pending'
            }
        }