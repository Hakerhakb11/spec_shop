from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.dependencies import get_async_db
from app.modules.users.models import User
from app.modules.users.repository import get_user_by_id

http_bearer = HTTPBearer(auto_error=True)


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_async_db)],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials

    user_id = decode_access_token(token=token)
    if not user_id:
        raise credentials_exception

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    return user
