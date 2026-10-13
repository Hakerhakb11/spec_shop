from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_async_db
from app.modules.auth.schemas import LoginRequest, TokenResponse
from app.modules.auth.service import login

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login_endpoint(
    db: Annotated[AsyncSession, Depends(get_async_db)], login_in: LoginRequest
):
    return await login(db, login_in)
