# Data — P8 Inventory & Stock Tracker

## Files

| File | What it is |
|---|---|
| `raw/inventory_SAMPLE.csv` | The 48 SAMPLE SKUs the workbook is built from |

## Columns (data dictionary)

| Column | Type | Meaning | Used by |
|---|---|---|---|
| SKU | text, unique | Stock code, e.g. `GR-002` (prefix = category) | Inventory key; Reorder List links back to it |
| Product | text | Product name | Inventory / Reorder List / Movements |
| Category | text | One of 5 categories (Groceries, Household, Electronics, Stationery, Personal Care) | Dashboard category chart (SUMIF) |
| Supplier | text | Supplier name for the SKU | Reference; shown on Inventory and Reorder List |
| Unit | text | Selling unit (bag, bottle, pack, piece, …) | Reference |
| Unit Cost (PKR) | integer > 0 | What the shop pays per unit | Stock Value (= Stock × Cost), Order Cost |
| Selling Price (PKR) | integer > Cost | What the shop sells it for | Margin % (= (Price − Cost) / Price) |
| Stock on Hand | integer ≥ 0 | Units currently on the shelves | Status, Stock Value, Dashboard KPIs |
| Reorder Point | integer | Stock level that triggers reordering | Status (LOW STOCK below it), Suggested Order Qty |
| Reorder Qty | integer | Supplier order quantity on file | Reference only — no formula uses it; Suggested Order Qty is Reorder Point × 2 − Stock on Hand (see README Limits) |
| Lead Time Days | integer | Days the supplier takes to deliver | Reference only — no formula uses it |

## About this data

**SAMPLE data, generated 4 Nov 2026** (`src/generate_sample_data.py`,
seed 42 — re-running reproduces the identical file). "PakStore" is a
fictional shop; no real business's stock is involved. The tracker —
the formulas, the status logic, the reorder sheet — is the product;
the numbers exist to prove it.

48 SKUs across 5 categories: Groceries (10), Household (10),
Electronics (9), Stationery (9), Personal Care (10). 3 SKUs are
deliberately out of stock and 8 deliberately below their reorder
point, so the Reorder List sheet has real content to show.
