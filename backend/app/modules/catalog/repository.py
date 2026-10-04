from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models import Category, Product


async def get_products(db: AsyncSession) -> list[Product]:
    statement = select(Product)

    result = await db.scalars(statement)
    return list(result.all())


async def get_categories(db: AsyncSession) -> list[Category]:
    statement = select(Category)

    result = await db.scalars(statement)
    return list(result.all())
