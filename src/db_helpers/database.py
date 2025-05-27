from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from config_loader import POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DBNAME

database_url = f"postgresql+psycopg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"

engine = create_async_engine(url=database_url, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

Base = declarative_base()