from pydantic import BaseModel, field_validator
from typing import Optional

# -----------------------
# ----- User Models -----


class SignUpModel(BaseModel):
    username: str
    email: Optional[str] = None
    password: str
    role: str
    is_verified: Optional[bool] = False
    is_active: Optional[bool] = False

    @field_validator("email", mode="before")
    def empty_str_to_none(cls, value):
        if isinstance(value, str):
            value = value.strip()
        return value or None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "summary": "Minimal input (optional fields excluded)",
                    "value": {
                        "username": "johndoe",
                        "password": "securepass",
                        "role": "user",
                    },
                },
                {
                    "summary": "Full input with all optional fields",
                    "value": {
                        "username": "johndoe",
                        "email": "johndoe@email.com",
                        "password": "securepass",
                        "role": "user",
                        "is_verified": False,
                        "is_active": False,
                    },
                },
            ]
        }


class LoginModel(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "securepass",
            }
        }


class UpdateModel(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = ""
    is_active: Optional[bool] = False

    @field_validator("email", mode="before")
    def empty_str_to_none(cls, value):
        if isinstance(value, str):
            value = value.strip()
        return value or None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "summary": "Update email",
                    "value": {"email": "johndoe@newemail.com"},
                },
                {
                    "summary": "Update password",
                    "value": {"password": "newsecurepass"},
                },
            ]
        }


# class DeleteModel(BaseModel):
#     username: str

#     class Config:
#         from_attributes = True
#         json_schema_extra = {
#             "example": {
#                 "username": "johndoe",
#             }
#         }


class Settings(BaseModel):
    authjwt_secret_key: str = "93ba757a8da35f4e1f933fc00af060fb1d970f84ec70d66259ad6db5ae3d1486"


# ------------------------
# ----- Order Models -----


class PlaceOrderModel(BaseModel):
    quantity: int
    order_status: str
    pizza_size: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "quantity": 1,
                "order_status": "received",
                "pizza_size": "medium",
            }
        }
