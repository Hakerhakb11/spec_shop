from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import password_hash
from app.modules.users.models import User
from app.modules.users.schemas import UserCreateRequest


async def get_user_by_email(
    db: AsyncSession,
    email: str,
) -> User | None:
    statement = select(User).where(User.email == email)

    return await db.scalar(statement)


async def get_user_by_id(db: AsyncSession, id: str) -> User | None:
    statement = select(User).where(User.id == id)

    return await db.scalar(statement)


async def create_user(db: AsyncSession, user_in: UserCreateRequest) -> User:
    if await get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email '{user_in.email}' already exists",
        )

    hashed_password = password_hash.hash(user_in.password)
    user = User(email=user_in.email, hashed_password=hashed_password)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
