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