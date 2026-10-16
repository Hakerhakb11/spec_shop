from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_async_db
from app.modules.auth.dependencies import get_current_user
from app.modules.catalog.repository import get_categories, get_products
from app.modules.catalog.schemas import (
    CategoryCreateRequest,
    CategoryResponse,
    ProductCreateRequest,
    ProductResponse,
)
from app.modules.catalog.service import create_category, create_product
from app.modules.users.models import User

router = APIRouter(prefix="/api/v1/catalog", tags=["Catalog"])


@router.get("/products", response_model=list[ProductResponse])
async def list_products(db: Annotated[AsyncSession, Depends(get_async_db)]):
    return await get_products(db)


@router.post(
    "/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED
)
async def create_product_endpoint(
    db: Annotated[AsyncSession, Depends(get_async_db)],
    product_in: ProductCreateRequest,
    _: Annotated[User, Depends(get_current_user)],
):
    return await create_product(db, product_in)


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(db: Annotated[AsyncSession, Depends(get_async_db)]):
    return await get_categories(db)


@router.post(
    "/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED
)
async def create_category_endpoint(
    db: Annotated[AsyncSession, Depends(get_async_db)],
    category_in: CategoryCreateRequest,
    _: Annotated[User, Depends(get_current_user)],
):
    return await create_category(db, category_in)
