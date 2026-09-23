"""
models.py
Defines the core data structures used across the Inventory Management System.
"""

from dataclasses import dataclass, field, asdict


@dataclass
class Product:
    """Represents a single product in the inventory."""
    product_id: str
    name: str
    category: str
    price: float
    quantity: int
    reorder_level: int = 5

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data: dict):
        return Product(
            product_id=data["product_id"],
            name=data["name"],
            category=data["category"],
            price=float(data["price"]),
            quantity=int(data["quantity"]),
            reorder_level=int(data.get("reorder_level", 5)),
        )

    def is_low_stock(self) -> bool:
        return self.quantity <= self.reorder_level

    def stock_value(self) -> float:
        return round(self.price * self.quantity, 2)


@dataclass
class Sale:
    """Represents a single recorded sale transaction."""
    sale_id: str
    product_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_amount: float
    timestamp: str

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data: dict):
        return Sale(
            sale_id=data["sale_id"],
            product_id=data["product_id"],
            product_name=data["product_name"],
            quantity=int(data["quantity"]),
            unit_price=float(data["unit_price"]),
            total_amount=float(data["total_amount"]),
            timestamp=data["timestamp"],
        )
