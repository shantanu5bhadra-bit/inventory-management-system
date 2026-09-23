# Inventory & Stock Management System

A console-based Inventory and Stock Management System built in Python, developed
as the "Build Your Own Project" submission for **CSE1021 – Introduction to
Problem Solving**.

## Overview

Small shops and stores often struggle to track stock levels, sales, and
reorder points manually, leading to stockouts or overstocking. This project
implements a menu-driven command-line application that lets a shop owner
manage products, track inventory movements, record sales, and generate
reports — all backed by reliable, persistent JSON storage.

## Features

- **Product Management** – add, update, delete, view, and search products
- **Inventory Operations** – stock in / stock out, automatic low-stock alerts
  based on a configurable reorder level
- **Sales Processing** – record a sale (validates and deducts available
  stock), generates a formatted receipt
- **Reporting & Analytics** – inventory valuation report, sales summary
  report, and top-selling-products ranking
- **Reliability** – atomic JSON writes so data is never corrupted mid-save
- **Robust validation & error handling** – no crashes on bad input; clear
  error messages
- **Logging** – every significant action (add, update, delete, stock
  change, sale) is timestamped and logged to `logs/app.log`

## Technologies / Tools Used

- Python 3 (standard library only — no external dependencies)
- `json` for persistent storage
- `logging` for audit-trail logging
- `unittest` for automated testing
- `dataclasses` for clean data models

## Project Structure

```
inventory_system/
├── main.py                     # CLI entry point / menu
├── modules/
│   ├── models.py                # Product & Sale data models
│   ├── data_manager.py          # JSON persistence (atomic writes)
│   ├── validators.py            # Input validation helpers
│   ├── logger_setup.py          # Logging configuration
│   ├── product_manager.py       # Module 1: Product CRUD
│   ├── inventory_manager.py     # Module 2: Stock in/out, low-stock alerts
│   ├── sales_manager.py         # Module 3a: Sales + receipts
│   └── report_manager.py        # Module 3b: Reports & analytics
├── tests/
│   ├── test_product_manager.py
│   └── test_inventory_and_sales.py
├── data/                        # products.json, sales.json (auto-created)
├── logs/                        # app.log (auto-created)
├── statement.md
└── README.md
```

## Steps to Install & Run

1. Ensure Python 3.8+ is installed:
   ```
   python3 --version
   ```
2. Clone or download this repository.
3. From the project root, run:
   ```
   python3 main.py
   ```
4. Use the on-screen numbered menu to manage products, stock, and sales.

No external packages are required — the project uses only the Python
standard library.

## Instructions for Testing

Run the automated unit test suite from the project root:

```
python3 -m unittest discover tests -v
```

This runs 12 unit tests covering product CRUD, validation failures, stock
in/out, low-stock detection, and sales processing (including insufficient
stock handling).

## Screenshots

*(Add screenshots of the running menu, a sale receipt, and a report here
before final submission.)*

## Author

Submitted for CSE1021 – Introduction to Problem Solving, VITyarthi
"Build Your Own Project" evaluation.
