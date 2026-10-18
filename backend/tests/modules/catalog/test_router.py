import pytest
from httpx import AsyncClient

from app.modules.catalog.models import Category, Product

pytestmark = pytest.mark.asyncio


async def test_list_categories_empty(client: AsyncClient):
    response = await client.get("api/v1/catalog/categories")

    assert response.status_code == 200
    assert response.json() == []


async def test_list_categories(client: AsyncClient, db_session):
    new_category = Category(name="Обувь", attributes_schema={})
    db_session.add(new_category)
    await db_session.commit()
    await db_session.refresh(new_category)

    response = await client.get("api/v1/catalog/categories")

    assert response.status_code == 200
    data = response.json()[0]
    assert data["name"] == "Обувь"
    assert data["attributes_schema"] == {}


async def test_list_products_empty(client: AsyncClient):
    response = await client.get("api/v1/catalog/products")

    assert response.status_code == 200
    assert response.json() == []


async def test_list_products_with_data(client: AsyncClient, db_session):
    new_category = Category(name="Обувь", attributes_schema={})
    db_session.add(new_category)
    await db_session.commit()
    await db_session.refresh(new_category)

    new_product = Product(title="Берцы", category_id=new_category.id, attributes={})
    db_session.add(new_product)
    await db_session.commit()

    response = await client.get("api/v1/catalog/products")

    assert response.status_code == 200
    data = response.json()[0]
    assert data["title"] == "Берцы"
    assert data["category_id"] == new_category.id
    assert data["attributes"] == {}


async def test_create_category_unauthorized(client: AsyncClient):
    response = await client.post(
        "/api/v1/catalog/categories",
        json={"name": "Обувь", "parent_id": None, "attributes_schema": {}},
    )
    assert response.status_code in (401, 403)


async def test_create_category_null_parent(auth_client: AsyncClient):
    response = await auth_client.post(
        "api/v1/catalog/categories",
        json={
            "name": "Обувь",
            "parent_id": None,
            "attributes_schema": {"size": "integer", "color": "string"},
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Обувь"
    assert data["parent_id"] is None
    assert data["attributes_schema"] == {"size": "integer", "color": "string"}
    assert "id" in data


async def test_create_category_nonexistent_parent(auth_client: AsyncClient):
    response = await auth_client.post(
        "api/v1/catalog/categories",
        json={"name": "Обувь", "parent_id": 99999, "attributes_schema": {}},
    )

    assert response.status_code in (400, 422, 404)


async def test_create_category_with_parent(auth_client: AsyncClient):
    parent_response = await auth_client.post(
        "/api/v1/catalog/categories",
        json={
            "name": "Обувь",
            "parent_id": None,
            "attributes_schema": {"size": "integer", "color": "string"},
        },
    )
    assert parent_response.status_code == 201
    parent_id = parent_response.json()["id"]

    child_response = await auth_client.post(
        "/api/v1/catalog/categories",
        json={
            "name": "Берцы",
            "parent_id": parent_id,
            "attributes_schema": {"season": "string"},
        },
    )

    assert child_response.status_code == 201
    child_data = child_response.json()

    assert child_data["name"] == "Берцы"
    assert child_data["parent_id"] == parent_id

    expected_schema = {"size": "integer", "color": "string", "season": "string"}
    assert child_data["attributes_schema"] == expected_schema
