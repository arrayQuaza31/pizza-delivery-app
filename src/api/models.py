from pydantic import BaseModel
from typing import Optional

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

class Settings(BaseModel):
    authjwt_secret_key: str = '93ba757a8da35f4e1f933fc00af060fb1d970f84ec70d66259ad6db5ae3d1486'

class LoginModel(BaseModel):
    username: str
    password: str