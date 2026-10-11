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
    assert response_second.status_code == 400

    error_data = response_second.json()
    assert "detail" in error_data
