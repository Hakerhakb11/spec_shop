from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_async_db
from app.modules.users.repository import create_user
from app.modules.users.schemas import UserCreateRequest, UserResponse

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post(
    "/create",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_endpoint(
    db: Annotated[AsyncSession, Depends(get_async_db)], user_in: UserCreateRequest
):
    return await create_user(db, user_in)
