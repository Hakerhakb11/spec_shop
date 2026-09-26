from typing import Annotated

from app.db.dependencies import get_async_db
from app.modules.catalog.repository import create_product, get_categories, get_products
from app.modules.catalog.schemas import ProductResponse
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/api/v1', tags=['Catalog'])


@router.get('/products', response_model=list[ProductResponse])
async def list_products(db: Annotated[AsyncSession, Depends(get_async_db)]):
    return await get_products(db)
