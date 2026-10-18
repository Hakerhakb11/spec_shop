import pytest
from httpx import AsyncClient

from app.core.security import hash_password
from app.modules.users.models import User

pytestmark = pytest.mark.asyncio


async def test_login_success(client: AsyncClient, test_user: User):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": test_user.email, "password": "secret123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(client: AsyncClient, test_user: User):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": test_user.email, "password": "wrongpassword"},
    )

    assert response.status_code == 401


async def test_login_nonexistent_email(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "secret123"},
    )

    assert response.status_code == 401


async def test_login_inactive_user(client: AsyncClient, db_session):
    inactive_user = User(
        email="banned@example.com",
        hashed_password=hash_password("secret123"),
        is_active=False,
    )
    db_session.add(inactive_user)
    await db_session.commit()

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "banned@example.com", "password": "secret123"},
    )

    assert response.status_code == 403


async def test_login_invalid_email_format(client: AsyncClient):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "bad-email-format", "password": "secretpassword123"},
    )

    assert response.status_code == 422
