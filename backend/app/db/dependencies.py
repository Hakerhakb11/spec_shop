from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import session_maker


async def get_async_db() -> AsyncGenerator[AsyncSession]:
    async with session_maker() as db:
        yield db
