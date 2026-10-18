from typing import Any

from pydantic import BaseModel, ConfigDict


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    parent_id: int | None = None
    attributes_schema: dict[str, Any] | None = None


class CategoryCreateRequest(BaseModel):
    name: str
    parent_id: int | None = None
    attributes_schema: dict[str, Any] | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category_id: int
    description: str | None = None
    attributes: dict[str, Any] | None = None


class ProductCreateRequest(BaseModel):
    title: str
    category_id: int
    description: str | None = None
    attributes: dict[str, Any] | None = None


class ProductVariantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    product_id: int
    price: int
    attributes: dict[str, Any] | None = None


class StoreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    address: str


class InventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    store_id: int
    product_variant_id: int
    quantity: int
