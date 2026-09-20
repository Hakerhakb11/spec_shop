from typing import Any

from app.db.base import Base
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id', ondelete='RESTRICT'),
        nullable=False,
    )
    category: Mapped['Category'] = relationship(back_populates='products')

    attributes: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey('categories.id', ondelete='RESTRICT'), default=None, nullable=True
    )
    products: Mapped[list['Product']] = relationship(back_populates='category')
    attributes_schema: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=True)


class ProductVariant(Base):
    __tablename__ = 'product_variants'

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id', ondelete='RESTRICT')
    )
    price: Mapped[int] = mapped_column(nullable=False)
    attributes: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)


class Store(Base):
    __tablename__ = 'stores'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)


class Inventory(Base):
    __tablename__ = 'inventories'

    store_id: Mapped[int] = mapped_column(
        ForeignKey('stores.id', ondelete='CASCADE'), primary_key=True
    )
    product_variant_id: Mapped[int] = mapped_column(
        ForeignKey('product_variants.id', ondelete='CASCADE'), primary_key=True
    )
    quantity: Mapped[int] = mapped_column(default=0)

    store: Mapped['Store'] = relationship(
        back_populates='inventory',
    )

    variant: Mapped['ProductVariant'] = relationship(
        back_populates='inventory',
    )
