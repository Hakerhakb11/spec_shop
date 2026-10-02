from typing import Any

from pydantic import BaseModel, ConfigDict


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    parent_id: int | None = None
    attributes_schema: dict[str, Any] | None


class CategoryCreateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    parent_id: int | None = None
    attributes_schema: dict[str, Any] | None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category_id: int
    description: str | None
    attributes: dict[str, Any] | None


class ProductCreateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    category_id: int
    description: str | None
    attributes: dict[str, Any] | None


class ProductVariantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sku: str
    product_id: int
    price: int
    attributes: dict[str, Any] | None


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
