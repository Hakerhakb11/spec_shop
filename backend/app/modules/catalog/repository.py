from app.modules.catalog.models import Product
from sqlalchemy import select
from sqlalchemy.orm import AsyncSession


async def get_products(db: AsyncSession) -> list[Product]:
    statement = select(Product)

    result = await db.scalars(statement)
    return list(result.all())
