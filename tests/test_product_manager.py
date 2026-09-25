"""
test_product_manager.py
Unit tests for the Product Management module.
Run with: python -m unittest discover tests
"""

import unittest
import os
import sys
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules import data_manager
from modules.product_manager import ProductManager
from modules.validators import ValidationError


class TestProductManager(unittest.TestCase):
    def setUp(self):
        # Redirect storage to a temp test file so tests don't touch real data
        self._orig_products_file = data_manager.PRODUCTS_FILE
        data_manager.PRODUCTS_FILE = os.path.join(data_manager.DATA_DIR, "test_products.json")
        if os.path.exists(data_manager.PRODUCTS_FILE):
            os.remove(data_manager.PRODUCTS_FILE)
        self.pm = ProductManager()

    def tearDown(self):
        if os.path.exists(data_manager.PRODUCTS_FILE):
            os.remove(data_manager.PRODUCTS_FILE)
        data_manager.PRODUCTS_FILE = self._orig_products_file

    def test_add_product_success(self):
        product = self.pm.add_product("Notebook", "Stationery", 2.5, 100, 10)
        self.assertEqual(product.name, "Notebook")
        self.assertEqual(len(self.pm.list_products()), 1)

    def test_add_product_empty_name_fails(self):
        with self.assertRaises(ValidationError):
            self.pm.add_product("", "Stationery", 2.5, 100)

    def test_add_product_negative_price_fails(self):
        with self.assertRaises(ValidationError):
            self.pm.add_product("Pen", "Stationery", -1, 100)

    def test_update_product(self):
        product = self.pm.add_product("Pen", "Stationery", 1.0, 50)
        updated = self.pm.update_product(product.product_id, price="1.5")
        self.assertEqual(updated.price, 1.5)

    def test_delete_product(self):
        product = self.pm.add_product("Eraser", "Stationery", 0.5, 30)
        self.pm.delete_product(product.product_id)
        self.assertIsNone(self.pm.find_product(product.product_id))

    def test_search_by_name(self):
        self.pm.add_product("Blue Pen", "Stationery", 1.0, 20)
        self.pm.add_product("Notebook", "Stationery", 2.0, 20)
        results = self.pm.search_by_name("pen")
        self.assertEqual(len(results), 1)


if __name__ == "__main__":
    unittest.main()
