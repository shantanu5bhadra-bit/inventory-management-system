"""
main.py
Inventory & Stock Management System -- CLI entry point.

CSE1021 (Introduction to Problem Solving) -- Build Your Own Project.

This console application ties together the three functional modules:
  1. Product Management (product_manager.py)
  2. Inventory Operations (inventory_manager.py)
  3. Sales & Reporting (sales_manager.py, report_manager.py)
"""

from modules.product_manager import ProductManager
from modules.inventory_manager import InventoryManager
from modules.sales_manager import SalesManager
from modules.report_manager import ReportManager
from modules.validators import ValidationError
from modules.logger_setup import get_logger

logger = get_logger(__name__)

MAIN_MENU = """
==================================================
        INVENTORY & STOCK MANAGEMENT SYSTEM
==================================================
 1. Add Product
 2. View All Products
 3. Search Product by Name
 4. Update Product
 5. Delete Product
 6. Stock In (add stock)
 7. Stock Out (remove stock)
 8. Record a Sale
 9. View Low Stock Alerts
10. Inventory Valuation Report
11. Sales Summary Report
12. Top Selling Products
 0. Exit
==================================================
"""


def print_products(products):
    if not products:
        print("No products found.")
        return
    print(f"{'ID':<10}{'Name':<20}{'Category':<15}{'Price':<10}{'Qty':<8}{'Reorder':<8}")
    print("-" * 71)
    for p in products:
        print(f"{p.product_id:<10}{p.name:<20}{p.category:<15}{p.price:<10.2f}{p.quantity:<8}{p.reorder_level:<8}")


def main():
    product_manager = ProductManager()
    inventory_manager = InventoryManager(product_manager)
    sales_manager = SalesManager(product_manager, inventory_manager)
    report_manager = ReportManager(product_manager, sales_manager)

    logger.info("Application started")

    while True:
        print(MAIN_MENU)
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                name = input("Product name: ")
                category = input("Category: ")
                price = input("Price: ")
                quantity = input("Initial quantity: ")
                reorder = input("Reorder level (default 5, press Enter to skip): ") or 5
                product = product_manager.add_product(name, category, price, quantity, reorder)
                print(f"Product added successfully. ID = {product.product_id}")

            elif choice == "2":
                print_products(product_manager.list_products())

            elif choice == "3":
                keyword = input("Enter name keyword to search: ")
                print_products(product_manager.search_by_name(keyword))

            elif choice == "4":
                pid = input("Enter product ID to update: ").strip()
                print("Leave a field blank to keep its current value.")
                name = input("New name: ")
                category = input("New category: ")
                price = input("New price: ")
                reorder = input("New reorder level: ")
                product = product_manager.update_product(
                    pid, name=name, category=category, price=price, reorder_level=reorder
                )
                print(f"Product {product.product_id} updated.")

            elif choice == "5":
                pid = input("Enter product ID to delete: ").strip()
                product_manager.delete_product(pid)
                print("Product deleted.")

            elif choice == "6":
                pid = input("Enter product ID: ").strip()
                qty = input("Quantity to add: ")
                product = inventory_manager.stock_in(pid, qty)
                print(f"Stock updated. {product.name} now has {product.quantity} units.")

            elif choice == "7":
                pid = input("Enter product ID: ").strip()
                qty = input("Quantity to remove: ")
                product = inventory_manager.stock_out(pid, qty)
                print(f"Stock updated. {product.name} now has {product.quantity} units.")

            elif choice == "8":
                pid = input("Enter product ID: ").strip()
                qty = input("Quantity sold: ")
                sale = sales_manager.record_sale(pid, qty)
                print(sales_manager.generate_receipt(sale))

            elif choice == "9":
                low_stock = inventory_manager.check_low_stock()
                if not low_stock:
                    print("All products are sufficiently stocked.")
                else:
                    print("LOW STOCK ALERT for the following products:")
                    print_products(low_stock)

            elif choice == "10":
                rows, total = report_manager.inventory_valuation_report()
                print(f"\n{'ID':<10}{'Name':<20}{'Qty':<8}{'Price':<10}{'Value':<10}")
                print("-" * 58)
                for r in rows:
                    print(f"{r[0]:<10}{r[1]:<20}{r[2]:<8}{r[3]:<10.2f}{r[4]:<10.2f}")
                print(f"\nTotal Inventory Value: {total:.2f}")

            elif choice == "11":
                rows, total = report_manager.sales_summary_report()
                if not rows:
                    print("No sales recorded yet.")
                else:
                    print(f"\n{'ID':<10}{'Name':<20}{'Qty Sold':<10}{'Revenue':<10}")
                    print("-" * 50)
                    for r in rows:
                        print(f"{r[0]:<10}{r[1]:<20}{r[2]:<10}{r[3]:<10.2f}")
                    print(f"\nTotal Revenue: {total:.2f}")

            elif choice == "12":
                top = report_manager.top_selling_products()
                if not top:
                    print("No sales recorded yet.")
                else:
                    print("\nTop Selling Products:")
                    for rank, r in enumerate(top, start=1):
                        print(f"{rank}. {r[1]} -- {r[2]} units sold, revenue {r[3]:.2f}")

            elif choice == "0":
                print("Exiting. Goodbye!")
                logger.info("Application exited normally")
                break

            else:
                print("Invalid choice. Please select a valid menu option.")

        except ValidationError as ve:
            print(f"Input error: {ve}")
            logger.warning(f"ValidationError: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            logger.error(f"Unexpected error: {e}", exc_info=True)


if __name__ == "__main__":
    main()
