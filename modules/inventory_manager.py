"""
inventory_manager.py
Functional Module 2: Inventory Operations (stock in/out, low-stock alerts).
"""

from modules.validators import validate_positive_int, ValidationError
from modules.logger_setup import get_logger

logger = get_logger(__name__)


class InventoryManager:
    def __init__(self, product_manager):
        self.product_manager = product_manager

    def stock_in(self, product_id, quantity):
        quantity = validate_positive_int(quantity, "Quantity")
        product = self.product_manager.find_product(product_id)
        if not product:
            raise ValidationError(f"No product found with ID {product_id}")
        product.quantity += quantity
        self.product_manager._persist()
        logger.info(f"Stock IN: {quantity} units added to {product_id}")
        return product

    def stock_out(self, product_id, quantity):
        quantity = validate_positive_int(quantity, "Quantity")
        product = self.product_manager.find_product(product_id)
        if not product:
            raise ValidationError(f"No product found with ID {product_id}")
        if quantity > product.quantity:
            raise ValidationError(
                f"Insufficient stock for {product.name}: only {product.quantity} left."
            )
        product.quantity -= quantity
        self.product_manager._persist()
        logger.info(f"Stock OUT: {quantity} units removed from {product_id}")
        return product

    def check_low_stock(self):
        """Returns list of products at or below their reorder level."""
        return [p for p in self.product_manager.list_products() if p.is_low_stock()]
