from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
# from fastapi_jwt_auth import AuthJWT
from typing import AsyncGenerator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import SignUpModel, LoginModel
from database.db_session import get_db_session
from database.models import User
from services.password_helper import generate_password_hash, verify_password


auth_router = APIRouter()


@auth_router.get('/')
async def hello():
    return {'message': 'Hello from auth'}


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(User).filter(User.username==user.username))
    db_user = result.scalars().first()
    if db_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='A user with this username already exists!'
        )
    result = await session.execute(select(User).filter(User.email==user.email))
    db_user = result.scalars().first()
    if db_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='A user with this email already exists!'
        )
    new_user = User(
        **user.model_dump(exclude={'password'}), 
        password=generate_password_hash(user.password)
    )
    session.add(new_user)
    await session.commit()
    return {"message": f"User with User ID '{new_user.id}' has been created!"}


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(user: LoginModel, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(User).filter(User.username==user.username))
    db_user = result.scalars().first()
    if db_user and verify_password(user.password, db_user.password):
        return {"message": f"Welcome {db_user.username}!"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Invalid username or password. Please provide the correct credentials and try again.'
    )