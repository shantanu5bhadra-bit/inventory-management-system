# Project Statement

## Problem Statement

Small shop owners and small-scale retailers frequently manage stock, sales,
and reordering manually using notebooks or basic spreadsheets. This leads to
common problems: stockouts of fast-moving items, overstocking of slow-moving
items, lost track of sales revenue, and no easy way to know which products
need to be reordered. There is a need for a simple, reliable tool that lets a
shop owner track products, stock levels, and sales without requiring
internet access, a database server, or specialized hardware.

## Scope of the Project

This project delivers a **console-based Inventory & Stock Management
System** in Python that:

- Maintains a catalog of products (name, category, price, quantity, reorder
  level)
- Tracks stock movements (stock received, stock sold/removed)
- Records sales transactions and generates receipts
- Alerts the user when a product's stock falls at or below its reorder level
- Produces reports: current inventory valuation, sales summary, and top
  sellers

The scope is intentionally limited to a single-user, single-location,
file-based (JSON) system appropriate for a small shop or as an academic
demonstration of core problem-solving and programming concepts — it does
not include multi-user accounts, a network/database backend, or a graphical
interface.

## Target Users

- Small shop owners / small retail businesses who need a lightweight way to
  track inventory and sales without expensive software
- Students and instructors evaluating this project as a demonstration of
  modular Python design, data validation, persistence, and reporting logic

## High-Level Features

1. **Product Management** — create, view, search, update, and delete
   product records
2. **Inventory Operations** — increase stock (restock) or decrease stock
   (usage/loss), with automatic low-stock alerting
3. **Sales & Reporting** — record sales (with automatic stock deduction and
   receipt generation), and generate inventory valuation, sales summary, and
   top-seller reports
