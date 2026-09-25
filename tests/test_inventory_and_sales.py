"""
test_inventory_and_sales.py
Unit tests for InventoryManager and SalesManager (stock control + sales logic).
Run with: python -m unittest discover tests
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import data_manager
from modules.product_manager import ProductManager
from modules.inventory_manager import InventoryManager
from modules.sales_manager import SalesManager
from modules.validators import ValidationError


class TestInventoryAndSales(unittest.TestCase):
    def setUp(self):
        self._orig_products_file = data_manager.PRODUCTS_FILE
        self._orig_sales_file = data_manager.SALES_FILE
        data_manager.PRODUCTS_FILE = os.path.join(data_manager.DATA_DIR, "test_products2.json")
        data_manager.SALES_FILE = os.path.join(data_manager.DATA_DIR, "test_sales2.json")
        for f in (data_manager.PRODUCTS_FILE, data_manager.SALES_FILE):
            if os.path.exists(f):
                os.remove(f)

        self.pm = ProductManager()
        self.im = InventoryManager(self.pm)
        self.sm = SalesManager(self.pm, self.im)
        self.product = self.pm.add_product("Marker", "Stationery", 3.0, 10, reorder_level=5)

    def tearDown(self):
        for f in (data_manager.PRODUCTS_FILE, data_manager.SALES_FILE):
            if os.path.exists(f):
                os.remove(f)
        data_manager.PRODUCTS_FILE = self._orig_products_file
        data_manager.SALES_FILE = self._orig_sales_file

    def test_stock_in_increases_quantity(self):
        updated = self.im.stock_in(self.product.product_id, 5)
        self.assertEqual(updated.quantity, 15)

    def test_stock_out_decreases_quantity(self):
        updated = self.im.stock_out(self.product.product_id, 4)
        self.assertEqual(updated.quantity, 6)

    def test_stock_out_insufficient_stock_raises(self):
        with self.assertRaises(ValidationError):
            self.im.stock_out(self.product.product_id, 999)

    def test_low_stock_detection(self):
        self.im.stock_out(self.product.product_id, 6)  # 10 - 6 = 4, <= reorder_level 5
        low_stock = self.im.check_low_stock()
        self.assertEqual(len(low_stock), 1)

    def test_record_sale_deducts_stock_and_creates_receipt(self):
        sale = self.sm.record_sale(self.product.product_id, 2)
        self.assertEqual(sale.total_amount, 6.0)
        self.assertEqual(self.pm.find_product(self.product.product_id).quantity, 8)
        receipt = self.sm.generate_receipt(sale)
        self.assertIn("RECEIPT", receipt)

    def test_record_sale_insufficient_stock_raises(self):
        with self.assertRaises(ValidationError):
            self.sm.record_sale(self.product.product_id, 999)


if __name__ == "__main__":
    unittest.main()
