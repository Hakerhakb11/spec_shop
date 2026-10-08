from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_async_db
from app.modules.catalog.repository import (
    create_category,
    create_product,
    get_categories,
    get_products,
)
from app.modules.catalog.schemas import (
    CategoryCreateRequest,
    CategoryResponse,
    ProductCreateRequest,
    ProductResponse,
)

router = APIRouter(prefix="/api/v1/catalog", tags=["Catalog"])


@router.get("/products", response_model=list[ProductResponse])
async def list_products(db: Annotated[AsyncSession, Depends(get_async_db)]):
    return await get_products(db)


@router.post(
    "/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED
)
async def create_product_endpoint(
    product_in: ProductCreateRequest, db: Annotated[AsyncSession, Depends(get_async_db)]
):
    return await create_product(product_in, db)


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(db: Annotated[AsyncSession, Depends(get_async_db)]):
    return await get_categories(db)


@router.post(
    "/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED
)
async def create_category_endpoint(
    category_in: CategoryCreateRequest,
    db: Annotated[AsyncSession, Depends(get_async_db)],
):
    return await create_category(category_in, db)
