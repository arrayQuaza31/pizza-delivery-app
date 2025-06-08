from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession

from api.models import SignUpModel, LoginModel, UpdateModel, DeleteModel
from database.db_session import get_db_session
from database.models import User
from utils.auth_utils import verify_password, create_token, decode_token
from services.user_services import UserServices
from api.dependencies import JWTAccessTokenBearer, JWTRefreshTokenBearer


user_router = APIRouter()

USER_SRV = UserServices()

security_access = JWTAccessTokenBearer()
security_refresh = JWTRefreshTokenBearer()


@user_router.get("/")
async def hello():
    return {"message": "Hello from auth"}


@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel, session: Annotated[AsyncSession, Depends(get_db_session)]):
    message = await USER_SRV.create_user(session=session, user=user)
    if message == "USERNAME TAKEN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists.",
        )
    if message == "DUPLICATE ACCOUNT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already created an account using this email.",
        )
    return {"message": message}


@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginModel, session: Annotated[AsyncSession, Depends(get_db_session)]):
    db_user = await USER_SRV.get_user(session=session, where_filter={"username": user.username})
    if db_user and verify_password(user.password, db_user.password):
        user_data = db_user.to_dict(include={"id", "username"})
        access_token = create_token(user_data=user_data)
        refresh_token = create_token(user_data=user_data, refresh_token_flag=True)
        if not (access_token and refresh_token):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Encountered an error while creating tokens. Please try again after some time.",
            )
        return {
            "message": f"Welcome {db_user.username}.",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_data": user_data,
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password. Please provide the correct credentials and try again.",
    )


@user_router.patch("/account/update", status_code=status.HTTP_200_OK)
async def update_account_details(user: UpdateModel, session: Annotated[AsyncSession, Depends(get_db_session)]):
    updated_account = await USER_SRV.update_user(session=session, update_data=user)
    if not updated_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No account with username '{user.username}' exists.",
        )
    return {"message": f"Hi {user.username}, your details have been updated."}


@user_router.delete("/account/delete", status_code=status.HTTP_200_OK)
async def delete_account(user: DeleteModel, session: Annotated[AsyncSession, Depends(get_db_session)]):
    deleted_account = await USER_SRV.delete_user(session=session, username=user.username)
    if not deleted_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No account with username '{user.username}' exists.",
        )
    return {"message": "Your account has been deleted."}


@user_router.get("/list/users", status_code=status.HTTP_200_OK)
async def list_multiple_users(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    token_payload: Annotated[dict, Depends(security_access)],
):
    users = await USER_SRV.get_multiple_users(session=session, order_by_cols=[("created_at", 1)])
    users_serialized = [*(user.to_dict(exclude={"password"}) for user in users)]
    return users_serialized


@user_router.get("/refresh-token", status_code=status.HTTP_200_OK)
async def generate_new_access_token(token_payload: Annotated[dict, Depends(security_refresh)]):
    user_data = token_payload["sub"]
    access_token = create_token(user_data=user_data)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Encountered an error while creating tokens. Please try again after some time.",
        )
    return {"new_access_token": access_token}
