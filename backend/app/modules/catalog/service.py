from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models import Category, Product
from app.modules.catalog.repository import (
    get_category_by_id,
    save_category,
    save_product,
)
from app.modules.catalog.schemas import CategoryCreateRequest, ProductCreateRequest


async def create_category(
    db: AsyncSession, category_in: CategoryCreateRequest
) -> Category:
    parent_category = None

    if category_in.parent_id is not None:
        parent_category = await get_category_by_id(db, category_in.parent_id)
        if not parent_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent category with id {category_in.parent_id} not found",
            )

    if parent_category and parent_category.attributes_schema:
        final_attributes = parent_category.attributes_schema | (
            category_in.attributes_schema or {}
        )
    else:
        final_attributes = category_in.attributes_schema

    category = Category(
        name=category_in.name,
        parent_id=category_in.parent_id,
        attributes_schema=final_attributes,
    )

    save_category(db, category)
    await db.commit()

    return category


async def create_product(db: AsyncSession, product_in: ProductCreateRequest) -> Product:
    category = await get_category_by_id(db, product_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {product_in.category_id} not found",
        )

    product = Product(
        title=product_in.title,
        category_id=product_in.category_id,
        description=product_in.description,
        attributes=product_in.attributes,
    )

    save_product(db, product)
    await db.commit()

    return product
