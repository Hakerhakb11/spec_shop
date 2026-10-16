from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    statement = select(User).where(User.email == email)

    return await db.scalar(statement)


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)

    return await db.scalar(statement)


async def save_user(db: AsyncSession, user: User) -> User:
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
