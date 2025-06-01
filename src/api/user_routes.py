from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
# from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import SignUpModel, LoginModel, UpdateModel, DeleteModel
from database.db_session import get_db_session
from database.models import User
from utils.password_helper import verify_password
from services.user_services import UserServices


user_router = APIRouter()

USER_SRV = UserServices()

@user_router.get('/')
async def hello():
    return {'message': 'Hello from auth'}

@user_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel, session: AsyncSession = Depends(get_db_session)):
    message = await USER_SRV.create_user(session=session, user=user)
    if message == "USERNAME TAKEN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='A user with this username already exists!'
        )
    if message == "DUPLICATE ACCOUNT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='You have already created an account using this email!'
        )
    return {"message": message}

@user_router.post('/login', status_code=status.HTTP_200_OK)
async def login(user: LoginModel, session: AsyncSession = Depends(get_db_session)):
    db_user = await USER_SRV.get_user(session=session, where_filter={'username': user.username})
    if db_user and verify_password(user.password, db_user.password):
        return {"message": f"Welcome {db_user.username}!"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Invalid username or password. Please provide the correct credentials and try again.'
    )

@user_router.put('/account/update', status_code=status.HTTP_200_OK)
async def update_account_details(user: UpdateModel, session: AsyncSession = Depends(get_db_session)):
    updated_account = await USER_SRV.update_user(session=session, update_data=user)
    if not updated_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'No account with username \'{user.username}\' exists!'
        )
    return {"message": f"Hi {user.username}, your details have been updated!"}

@user_router.delete('/account/delete', status_code=status.HTTP_200_OK)
async def delete_account(user: DeleteModel, session: AsyncSession = Depends(get_db_session)):
    deleted_account = await USER_SRV.delete_user(session=session, username=user.username)
    if not deleted_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'No account with username \'{user.username}\' exists!'
        )
    return {"message": "Your account has been deleted!"}