from app.modules.catalog.models import Product
from sqlalchemy import select
from sqlalchemy.orm import Session


async def get_products(db: Session) -> list[Product]:
    statement = select(Product)

    result = await db.scalars(statement)
    return list(result.all())
