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


async def get_category_by_id(db: AsyncSession, category_id: int) -> Category | None:
    statement = select(Category).where(Category.id == category_id)

    return await db.scalar(statement)


async def save_category(db: AsyncSession, category: Category) -> Category:
    db.add(category)
    await db.flush()
    await db.refresh(category)
    return category


async def save_product(db: AsyncSession, product: Product) -> Product:
    db.add(product)
    await db.flush()
    await db.refresh(product)
    return product
