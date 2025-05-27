from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from typing import AsyncGenerator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import generate_password_hash
from api.models import SignUpModel
from db_helpers.database import AsyncSessionLocal
from db_helpers.models import User

auth_router = APIRouter(
    prefix='/auth', 
    tags=['auth']
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    # Yields an AsyncSession instance or None (after completion)
    async with AsyncSessionLocal() as session:
        yield session

@auth_router.get('/')
async def hello():
    return {'message': 'Hello from auth'}

@auth_router.post('/signup')
async def signup(user: SignUpModel, session: AsyncSession=Depends(get_db_session)):
    result = await session.execute(select(User).filter(User.username==user.username))
    db_username = result.scalars().first()
    if db_username is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='A user with this username already exists!'
        )
    result = await session.execute(select(User).filter(User.email==user.email))
    db_email = result.scalars().first()
    if db_email is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='A user with this email already exists!'
        )
    new_user = User(
        **user.model_dump(exclude={'password'}), 
        password=generate_password_hash(user.password)
    )
    session.add(new_user)
    await session.commit()
    return HTTPException(
        status_code=status.HTTP_201_CREATED, 
        detail=f"User with User ID '{new_user.id}' has been created!"
    )