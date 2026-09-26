from typing import Annotated

from app.db.dependencies import get_async_db
from app.modules.products.repository import get_products
from app.modules.products.schemas import ProductResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix='/api/v1/products', tags=['Products'])


@router.get('/', response_model=list[ProductResponse])
async def list_products(db: Annotated[Session, Depends(get_async_db)]):
    return await get_products(db)
