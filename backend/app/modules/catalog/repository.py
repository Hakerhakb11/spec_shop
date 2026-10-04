from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models import Category, Product
from app.modules.catalog.schemas import CategoryCreateRequest, ProductCreateRequest


async def get_products(db: AsyncSession) -> list[Product]:
    statement = select(Product)

    result = await db.scalars(statement)
    return list(result.all())


async def get_categories(db: AsyncSession) -> list[Category]:
    statement = select(Category)

    result = await db.scalars(statement)
    return list(result.all())


async def create_category(
    category_in: CategoryCreateRequest, db: AsyncSession
) -> Category:
    category = Category(
        name=category_in.name,
        parent_id=category_in.parent_id,
        attributes_schema=category_in.attributes_schema,
    )

    db.add(category)
    await db.commit()
    await db.refresh(category)

    return category


async def create_product(product_in: ProductCreateRequest, db: AsyncSession) -> Product:
    product = Product(
        title=product_in.title,
        category_id=product_in.category_id,
        description=product_in.description,
        attributes=product_in.attributes,
    )

    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product
