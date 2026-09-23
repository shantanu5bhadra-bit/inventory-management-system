"""
report_manager.py
Functional Module 3 (part B): Reporting & Analytics.
"""

from collections import defaultdict


class ReportManager:
    def __init__(self, product_manager, sales_manager):
        self.product_manager = product_manager
        self.sales_manager = sales_manager

    def inventory_valuation_report(self):
        """Returns (per-product list, grand total value of current stock)."""
        products = self.product_manager.list_products()
        rows = [(p.product_id, p.name, p.quantity, p.price, p.stock_value()) for p in products]
        grand_total = round(sum(r[4] for r in rows), 2)
        return rows, grand_total

    def low_stock_report(self):
        return [
            (p.product_id, p.name, p.quantity, p.reorder_level)
            for p in self.product_manager.list_products()
            if p.is_low_stock()
        ]

    def sales_summary_report(self):
        """Aggregates total quantity sold and revenue per product."""
        summary = defaultdict(lambda: {"name": "", "quantity": 0, "revenue": 0.0})
        for sale in self.sales_manager.list_sales():
            entry = summary[sale.product_id]
            entry["name"] = sale.product_name
            entry["quantity"] += sale.quantity
            entry["revenue"] += sale.total_amount

        rows = [
            (pid, data["name"], data["quantity"], round(data["revenue"], 2))
            for pid, data in summary.items()
        ]
        grand_total = round(sum(r[3] for r in rows), 2)
        return rows, grand_total

    def top_selling_products(self, n=3):
        rows, _ = self.sales_summary_report()
        return sorted(rows, key=lambda r: r[2], reverse=True)[:n]
