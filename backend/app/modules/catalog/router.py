from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_async_db
from app.modules.catalog.repository import get_categories, get_products
from app.modules.catalog.schemas import CategoryResponse, ProductResponse

router = APIRouter(prefix="/api/v1", tags=["Catalog"])


@router.get("/products", response_model=list[ProductResponse])
async def list_products(db: Annotated[AsyncSession, Depends(get_async_db)]):
    return await get_products(db)


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(db: Annotated[AsyncSession, Depends(get_async_db)]):
    return await get_categories(db)
