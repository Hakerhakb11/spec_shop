from fastapi import HTTPException, status
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


async def get_categories_by_id(
    db: AsyncSession, category_id: int | None
) -> Category | None:
    statement = select(Category).where(Category.id == category_id)

    result = await db.scalars(statement)
    return result.first()


async def create_category(
    category_in: CategoryCreateRequest, db: AsyncSession
) -> Category:
    parent_category = None

    if category_in.parent_id is not None:
        parent_category = await get_categories_by_id(db, category_in.parent_id)
        if not parent_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent category with id {category_in.parent_id} not found",
            )

    if parent_category and parent_category.attributes_schema:
        final_attributes = (
            parent_category.attributes_schema | category_in.attributes_schema
        )
    else:
        final_attributes = category_in.attributes_schema

    category = Category(
        name=category_in.name,
        parent_id=category_in.parent_id,
        attributes_schema=final_attributes,
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
