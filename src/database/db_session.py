from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from database.init_db import engine
from typing import AsyncGenerator

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    # Yields an AsyncSession instance or None (after completion)
    async with AsyncSessionLocal() as session:
        yield session
