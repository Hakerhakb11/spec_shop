import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models import Category, Product
from app.modules.catalog.repository import get_categories, get_products

pytestmark = pytest.mark.asyncio


async def test_get_categories_empty(db_session: AsyncSession):
    categories = await get_categories(db_session)
    assert categories == []


async def test_get_categories_with_data(db_session: AsyncSession):
    new_category = Category(name="Обувь", attributes_schema={})
    db_session.add(new_category)
    await db_session.commit()

    categories = await get_categories(db_session)
    assert categories[0].name == "Обувь"
    assert categories[0].attributes_schema == {}
    assert len(categories) == 1


async def test_get_products_empty(db_session: AsyncSession):
    products = await get_products(db_session)
    assert products == []


async def test_get_products_with_data(db_session: AsyncSession):
    new_category = Category(name="Обувь", attributes_schema={})
    db_session.add(new_category)
    await db_session.commit()
    await db_session.refresh(new_category)

    new_product = Product(title="Берцы", category_id=new_category.id, attributes={})
    db_session.add(new_product)
    await db_session.commit()

    products = await get_products(db_session)
    assert products[0].title == "Берцы"
    assert products[0].category_id == new_category.id
    assert products[0].attributes == {}
    assert len(products) == 1
