"""
data_manager.py
Handles all persistent storage (JSON file I/O) for the system.
Uses atomic writes (write to temp file then replace) so a crash mid-save
never corrupts the data files -- supports the Reliability requirement.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
SALES_FILE = os.path.join(DATA_DIR, "sales.json")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_json(filepath, default):
    _ensure_data_dir()
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return default
            return json.loads(content)
    except (json.JSONDecodeError, OSError):
        # Corrupt or unreadable file -- fail safe with empty default
        return default


def _save_json_atomic(filepath, data):
    _ensure_data_dir()
    tmp_path = filepath + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp_path, filepath)  # atomic on POSIX and Windows


def load_products():
    return _load_json(PRODUCTS_FILE, [])


def save_products(products_list_of_dicts):
    _save_json_atomic(PRODUCTS_FILE, products_list_of_dicts)


def load_sales():
    return _load_json(SALES_FILE, [])


def save_sales(sales_list_of_dicts):
    _save_json_atomic(SALES_FILE, sales_list_of_dicts)
