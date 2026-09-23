"""
product_manager.py
Functional Module 1: Product Management (CRUD operations).
"""

import uuid
from modules import data_manager
from modules.models import Product
from modules.validators import (
    validate_non_empty_string,
    validate_positive_float,
    validate_positive_int,
    ValidationError,
)
from modules.logger_setup import get_logger

logger = get_logger(__name__)


class ProductManager:
    def __init__(self):
        self.products = self._load()

    def _load(self):
        raw = data_manager.load_products()
        return [Product.from_dict(p) for p in raw]

    def _persist(self):
        data_manager.save_products([p.to_dict() for p in self.products])

    def add_product(self, name, category, price, quantity, reorder_level=5):
        name = validate_non_empty_string(name, "Product name")
        category = validate_non_empty_string(category, "Category")
        price = validate_positive_float(price, "Price")
        quantity = validate_positive_int(quantity, "Quantity")
        reorder_level = validate_positive_int(reorder_level, "Reorder level")

        product = Product(
            product_id=str(uuid.uuid4())[:8],
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            reorder_level=reorder_level,
        )
        self.products.append(product)
        self._persist()
        logger.info(f"Added product {product.product_id} ({product.name})")
        return product

    def find_product(self, product_id):
        for p in self.products:
            if p.product_id == product_id:
                return p
        return None

    def search_by_name(self, keyword: str):
        keyword = keyword.strip().lower()
        return [p for p in self.products if keyword in p.name.lower()]

    def update_product(self, product_id, **fields):
        product = self.find_product(product_id)
        if not product:
            raise ValidationError(f"No product found with ID {product_id}")

        if "name" in fields and fields["name"]:
            product.name = validate_non_empty_string(fields["name"], "Product name")
        if "category" in fields and fields["category"]:
            product.category = validate_non_empty_string(fields["category"], "Category")
        if "price" in fields and fields["price"] not in (None, ""):
            product.price = validate_positive_float(fields["price"], "Price")
        if "reorder_level" in fields and fields["reorder_level"] not in (None, ""):
            product.reorder_level = validate_positive_int(fields["reorder_level"], "Reorder level")

        self._persist()
        logger.info(f"Updated product {product_id}")
        return product

    def delete_product(self, product_id):
        product = self.find_product(product_id)
        if not product:
            raise ValidationError(f"No product found with ID {product_id}")
        self.products.remove(product)
        self._persist()
        logger.info(f"Deleted product {product_id}")

    def list_products(self):
        return list(self.products)
