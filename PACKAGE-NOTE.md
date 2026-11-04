# P8 — Package Note (Fiverr-ready)

**Gig title:** I will build your inventory and stock tracker that tells you what to reorder

**What the client gets:** one Excel workbook that answers, at a
glance, what they have in stock, what it is worth, what is running
low, and what exactly to order next — a Dashboard with live KPIs and
a stock-value-by-category chart, an Inventory sheet where Stock Value,
Margin % and OUT OF STOCK / LOW STOCK / OK status are all formulas,
and a Reorder List that builds itself from the low and out items with
a suggested order quantity and order cost per line. No more notebook
counts, no more discovering a product is gone when a customer asks
for it.

## Tiers (Hashir's band)

| Tier | Price | Delivery | Includes |
|---|---|---|---|
| Basic | $20 | 2 days | Inventory tracker in Excel for up to 50 SKUs: Dashboard KPIs + Inventory sheet with live Stock Value, Margin % and Status formulas |
| Standard | $65 | 3 days | Up to 200 SKUs, Reorder List sheet with suggested quantities and order costs, stock movements log, category chart, setup guide so the client maintains it themselves |
| Premium | $140 | 5 days | Unlimited SKUs, supplier + lead-time tracking, low-stock alert rules, monthly stock valuation report, Google Sheets version, reusable builder script for the client's own future stock lists, 1 revision round |

**What's NOT included:** a barcode/POS integration (quoted on seeing
the system); a Power BI dashboard (that's the P3 service); cleaning a
messy source stock file first (that's the P2 data-cleaning service —
quoted together if needed).

**Delivery time note:** counts from the day the client uploads their
stock list, not from order placement.

**Proof this service works:** this repo's sample — 48 SKUs across 5
categories for fictional shop PakStore, total stock value
PKR 1,162,496, 8 low-stock and 3 out-of-stock items caught by formula
and listed on a Reorder List totalling PKR 191,760 to order, 35
automated checks passing. The sample workbook is the demo the buyer
sees before ordering.
