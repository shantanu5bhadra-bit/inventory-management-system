"""
sales_manager.py
Functional Module 3 (part A): Sales processing.
Records a sale, deducts stock via InventoryManager, and generates a receipt.
"""

import uuid
from datetime import datetime
from modules import data_manager
from modules.models import Sale
from modules.validators import validate_positive_int, ValidationError
from modules.logger_setup import get_logger

logger = get_logger(__name__)


class SalesManager:
    def __init__(self, product_manager, inventory_manager):
        self.product_manager = product_manager
        self.inventory_manager = inventory_manager
        self.sales = self._load()

    def _load(self):
        raw = data_manager.load_sales()
        return [Sale.from_dict(s) for s in raw]

    def _persist(self):
        data_manager.save_sales([s.to_dict() for s in self.sales])

    def record_sale(self, product_id, quantity):
        quantity = validate_positive_int(quantity, "Quantity")
        product = self.product_manager.find_product(product_id)
        if not product:
            raise ValidationError(f"No product found with ID {product_id}")

        # This raises ValidationError if stock is insufficient
        self.inventory_manager.stock_out(product_id, quantity)

        total = round(product.price * quantity, 2)
        sale = Sale(
            sale_id=str(uuid.uuid4())[:8],
            product_id=product.product_id,
            product_name=product.name,
            quantity=quantity,
            unit_price=product.price,
            total_amount=total,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self.sales.append(sale)
        self._persist()
        logger.info(f"Sale recorded: {sale.sale_id} ({quantity} x {product.name})")
        return sale

    @staticmethod
    def generate_receipt(sale: Sale) -> str:
        lines = [
            "----------- RECEIPT -----------",
            f"Sale ID   : {sale.sale_id}",
            f"Date      : {sale.timestamp}",
            f"Product   : {sale.product_name}",
            f"Quantity  : {sale.quantity}",
            f"Unit Price: {sale.unit_price:.2f}",
            f"Total     : {sale.total_amount:.2f}",
            "--------------------------------",
        ]
        return "\n".join(lines)

    def list_sales(self):
        return list(self.sales)
