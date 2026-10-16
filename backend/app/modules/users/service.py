from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.modules.users.models import User
from app.modules.users.repository import get_user_by_email, save_user
from app.modules.users.schemas import UserCreateRequest


async def register_user(db: AsyncSession, user_in: UserCreateRequest) -> User:
    if await get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user_in.email}' already exists",
        )

    hashed_password = hash_password(user_in.password)
    user = User(email=user_in.email, hashed_password=hashed_password)

    save_user(db, user)
    await db.commit()
    return user
