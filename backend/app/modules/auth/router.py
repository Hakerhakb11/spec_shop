from fastapi import APIRouter

from app.db.dependencies import SessionDep
from app.modules.auth.schemas import LoginRequest, TokenResponse
from app.modules.auth.service import login

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login_endpoint(db: SessionDep, login_in: LoginRequest):
    return await login(db, login_in)
