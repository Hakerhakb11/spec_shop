from typing import Any

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), default=None, nullable=True
    )
    attributes_schema: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, nullable=True
    )
    products: Mapped[list[Product]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    attributes: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    category: Mapped[Category] = relationship(back_populates="products")
    product_variants: Mapped[list[ProductVariant]] = relationship(
        back_populates="product"
    )


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"), nullable=False
    )
    price: Mapped[int] = mapped_column(nullable=False)

    attributes: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB, default=dict, nullable=True
    )

    product: Mapped[Product] = relationship(back_populates="product_variants")
    inventories: Mapped[list[Inventory]] = relationship(
        back_populates="product_variant"
    )


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)

    inventories: Mapped[list[Inventory]] = relationship(back_populates="store")


class Inventory(Base):
    __tablename__ = "inventories"

    store_id: Mapped[int] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"), primary_key=True, nullable=False
    )
    product_variant_id: Mapped[int] = mapped_column(
        ForeignKey("product_variants.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(default=0, nullable=False)

    store: Mapped[Store] = relationship(
        back_populates="inventories",
    )

    product_variant: Mapped[ProductVariant] = relationship(
        back_populates="inventories",
    )
