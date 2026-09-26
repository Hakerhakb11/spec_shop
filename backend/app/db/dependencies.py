from collections.abc import AsyncGenerator

from app.db.database import session_maker
from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_db() -> AsyncGenerator[AsyncSession]:
    async with session_maker() as db:
        yield db
