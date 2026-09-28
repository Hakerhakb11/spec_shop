import pytest
from httpx import AsyncClient

from app.modules.catalog.models import Category, Product

pytestmark = pytest.mark.asyncio


async def test_list_categories_empty(client: AsyncClient):
    response = await client.get('api/v1/categories')

    assert response.status_code == 200
    assert response.json() == []


async def test_list_categories(client: AsyncClient, db_session):
    new_category = Category(name='Обувь', attributes_schema={})
    db_session.add(new_category)
    await db_session.commit()
    await db_session.refresh(new_category)

    response = await client.get('api/v1/categories')

    assert response.status_code == 200
    data = response.json()[0]
    assert data['name'] == 'Обувь'
    assert data['attributes_schema'] == {}


async def test_list_products_empty(client: AsyncClient):
    response = await client.get('api/v1/products')

    assert response.status_code == 200
    assert response.json() == []


async def test_list_products_with_data(client: AsyncClient, db_session):
    new_category = Category(name='Обувь', attributes_schema={})
    db_session.add(new_category)
    await db_session.commit()
    await db_session.refresh(new_category)

    new_product = Product(title='Берцы', category_id=new_category.id, attributes={})
    db_session.add(new_product)
    await db_session.commit()

    response = await client.get('api/v1/products')

    assert response.status_code == 200
    data = response.json()[0]
    assert data['title'] == 'Берцы'
    assert data['category_id'] == new_category.id
    assert data['attributes'] == {}
