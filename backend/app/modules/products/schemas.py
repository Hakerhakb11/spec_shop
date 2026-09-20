from typing import Any

from pydantic import BaseModel, ConfigDict


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    parent_id: int | None = None
    attributes_schema: dict


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category_id: int
    description: str | None
    attributes: dict[str, Any]


class ProductVariantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    product_id: int
    price: int
    attributes: dict[str, Any]


class StoreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    address: str


class InventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    store_id: int
    variant_id: int
    quantity: int
