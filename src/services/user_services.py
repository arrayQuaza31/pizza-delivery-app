from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from api.models import SignUpModel, UpdateModel
from utils.password_helper import generate_password_hash
from utils.query_builder import build_select_query


class UserServices:
    async def create_user(self, session: AsyncSession, user: SignUpModel) -> str:
        if await self.get_user(session=session, where_filter={"username": user.username}):
            return "USERNAME TAKEN"
        if user.email and await self.get_user(session=session, where_filter={"email": user.email}):
            return "DUPLICATE ACCOUNT"
        new_user = User(**user.model_dump(exclude={"password"}), password=generate_password_hash(user.password))
        session.add(new_user)
        await session.commit()
        return f"User with User ID '{new_user.id}' has been created!"

    async def get_user(self, session: AsyncSession, where_filter: dict = {}) -> Optional[User]:
        result = await session.execute(build_select_query(model=User, where_filter=where_filter))
        db_user = result.scalars().first()
        return db_user

    async def get_multiple_users(
        self, session: AsyncSession, where_filter: dict = {}, order_by_cols: list[dict] = []
    ) -> list[User]:
        result = await session.execute(
            build_select_query(model=User, where_filter=where_filter, order_by_cols=order_by_cols)
        )
        db_users = result.scalars().all()
        return db_users

    async def update_user(self, session: AsyncSession, update_data: UpdateModel) -> Optional[User]:
        existing_user = await self.get_user(session=session, where_filter={"username": update_data.username})
        if not existing_user:
            return None
        # print("Data to be Updated -->", update_data.model_dump())
        for field, value in update_data.model_dump(exclude={"username"}).items():
            if not value:
                continue
            if field == "password":
                value = generate_password_hash(value)
            setattr(existing_user, field, value)
        await session.commit()
        return existing_user

    async def delete_user(self, session: AsyncSession, username: str) -> bool:
        existing_user = await self.get_user(session=session, where_filter={"username": username})
        if not existing_user:
            return False
        await session.delete(existing_user)
        await session.commit()
        return True
