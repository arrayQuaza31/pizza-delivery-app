from sqlalchemy.ext.asyncio import create_async_engine
from config_loader import Config
from database.models import Base

database_url = f"postgresql+psycopg://{Config.POSTGRES_USERNAME}:{Config.POSTGRES_PASSWORD}@{Config.POSTGRES_HOST}:{Config.POSTGRES_PORT}/{Config.POSTGRES_DBNAME}"

engine = create_async_engine(url=database_url, echo=True)


async def init_db_models():
    async with engine.begin() as conn:
        from database.models import User, Order

        await conn.run_sync(Base.metadata.create_all)
    print("All database tables have been created!")
