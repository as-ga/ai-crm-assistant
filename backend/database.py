from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()


DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost:5432/ai_assistant"

# Create the async engine
engine = create_async_engine(os.getenv("DATABASE_URL"), echo=True)
# engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
