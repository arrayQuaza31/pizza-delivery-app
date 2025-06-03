from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine
from config_loader import Config
from database.models import Base


database_url = URL.create(
    drivername="postgresql+psycopg",
    username=Config.POSTGRES_USERNAME,
    password=Config.POSTGRES_PASSWORD,
    host=Config.POSTGRES_HOST,
    port=Config.POSTGRES_PORT,
    database=Config.POSTGRES_DBNAME,
)

engine = create_async_engine(url=database_url, echo=True)


async def init_db_models():
    async with engine.begin() as conn:
        from database.models import User, Order

        await conn.run_sync(Base.metadata.create_all)
    print("All database tables have been created!")
