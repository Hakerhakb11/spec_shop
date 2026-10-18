import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_create_user_success(client: AsyncClient):
    response = await client.post(
        "/api/v1/users/create",
        json={"email": "test@example.com", "password": "securepassword123"},
    )

    assert response.status_code == 201

    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert data["is_active"] is True
    assert "hashed_password" not in data
    assert "password" not in data


async def test_create_user_duplicate_email(client: AsyncClient):
    payload = {"email": "duplicate@example.com", "password": "password123"}

    response_first = await client.post("/api/v1/users/create", json=payload)
    assert response_first.status_code == 201

    response_second = await client.post("/api/v1/users/create", json=payload)
    assert response_second.status_code == 409

    error_data = response_second.json()
    assert "detail" in error_data


async def test_read_users_me_success(auth_client: AsyncClient, test_user):
    response = await auth_client.get("/api/v1/users/me")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email
    assert data["is_active"] is True


async def test_read_users_me_unauthorized(client: AsyncClient):
    response = await client.get("/api/v1/users/me")

    assert response.status_code in (401, 403)


async def test_create_user_invalid_email(client: AsyncClient):
    response = await client.post(
        "/api/v1/users/create",
        json={"email": "not-an-email", "password": "securepassword123"},
    )

    assert response.status_code == 422


async def test_create_user_short_password(client: AsyncClient):
    response = await client.post(
        "/api/v1/users/create",
        json={"email": "valid@example.com", "password": "short"},
    )

    assert response.status_code == 422


async def test_create_user_long_password(client: AsyncClient):
    response = await client.post(
        "/api/v1/users/create",
        json={"email": "valid@example.com", "password": "a" * 129},
    )

    assert response.status_code == 422
