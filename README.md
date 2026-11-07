# P8 — Inventory & Stock Tracker

**Client pain:** a small shop owner knows roughly what is on the
shelves but not exactly — stock counts live in a notebook, nobody
notices a product has run out until a customer asks for it, and
reorder decisions are guesses made at the supplier's counter.
**This delivery:** one workbook that answers, at a glance, what you
have, what it is worth, what is running low, and what to order next.
**Status: SAMPLE delivery**
**Tools:** Excel (live formulas + native chart) · Python (openpyxl
builder)
**Deliverable:** `outputs/inventory_tracker_SAMPLE.xlsx` (Dashboard +
Inventory + Reorder List + Movements, 48 SKUs, 5 categories)

> ⚠️ **What this is and is not.** "PakStore" is a fictional shop and
> all 48 SKUs are generated SAMPLE data (`src/generate_sample_data.py`,
> seed 42 — re-running reproduces the identical file). What is real
> is the tracker: every number on Dashboard is a live formula over the
> Inventory sheet, every Status is decided by a formula from Stock vs
> Reorder Point, and every Reorder List row is linked back to its
> Inventory row — so changing a stock level updates the dashboard,
> the statuses and the order list with nothing re-typed. The Movements
> sheet is a sample log only: it does NOT feed back into Inventory
> stock levels, and there is no live running balance there — the
> sheet says so itself.

## Business question it answers

> "What do I have in stock, what is it worth, what is about to run
> out, and what exactly should I order — without counting shelves by
> hand every week?"

## What is inside

| File | What it does |
|---|---|
| `outputs/inventory_tracker_SAMPLE.xlsx` | The deliverable: Dashboard (KPIs + category chart, all formulas) + Inventory (48 SKUs, Excel Table, live Stock Value / Margin % / Status) + Reorder List (11 items, live Suggested Order Qty + Order Cost) + Movements (30 sample Oct 2026 in/out rows, log only) |
| `data/raw/inventory_SAMPLE.csv` | The 48 SAMPLE SKUs the workbook is built from |
| `src/generate_sample_data.py` | Generates the sample CSV (deterministic, seed 42) |
| `src/build_tracker.py` | Builds the workbook: Inventory table, live-formula Dashboard/Reorder List, native chart, Movements log |
| `src/checks.py` | Data-quality checks as code — 35 checks, all passing |
| `requirements.txt` | Pinned dependency: `openpyxl==3.1.2` (verified with Python 3.12) |

## How it fits together

```
data/raw/inventory_SAMPLE.csv ──▶ src/build_tracker.py ──▶ outputs/inventory_tracker_SAMPLE.xlsx
(sample data, seed 42)              (openpyxl)             Dashboard / Inventory / Reorder List / Movements
                                                                    ▲ src/checks.py verifies all of it
```

## Limits — what this tracker does not do

- **Movements is a log only.** It does not change Inventory stock
  levels and there is no live running balance on that sheet.
- **Suggested Order Qty = Reorder Point × 2 − Stock on Hand.** The
  `Reorder Qty` and `Lead Time Days` columns on the Inventory sheet
  are reference data (supplier / lead-time tracking); no formula
  uses them, so changing them does not change the suggested order.
- **No barcode / POS integration** and no automatic supplier order —
  the Reorder List is the list the owner orders from.
- **One shop, PKR only.** Prices, costs and stock values are all in
  Pakistani rupees; the sample covers 48 SKUs in 5 categories.
- **Open it in Excel or Google Sheets to see the numbers.** The
  workbook carries live formulas (openpyxl writes formulas, not
  cached values), so they calculate when the file is opened — a raw
  file reader that does not calculate formulas will show blanks
  instead of KPI values.

## 3 key findings (from this sample)

1. **Electronics carries over a third of the money on the shelves.**
   Electronics is PKR 415,589 of the PKR 1,162,496 total stock value
   (35.7%) — and the single biggest line is Bluetooth Earbuds
   (EL-004, PKR 162,191). *So what:* the category chart sits on the
   Dashboard, not buried, because "where is my money tied up" is the
   first question a shop owner asks.
2. **11 of 48 SKUs need ordering now — 3 are already gone.** Tea
   Leaves 500g, Scrub Sponge and Colour Pencils are out of stock, and
   8 more sit below their reorder point (Cooking Oil 5L is down to 2
   against a reorder point of 11). *So what:* the Reorder List sheet
   exists so the owner orders from one list instead of walking the
   shelves, and its Suggested Order Qty already totals PKR 191,760 of
   stock to buy.
3. **Margins are thinnest where the money moves fastest.** Cooking Oil
   5L, a daily staple, keeps only 15.2% margin, while USB Cable 1m
   keeps 31.3%. *So what:* the Margin % column is on the Inventory
   sheet itself, because a reorder decision without a margin check is
   how a shop restocks its least profitable line first.

## Verified numbers

| KPI | Value |
|---|---|
| Total SKUs | 48 (Groceries 10, Household 10, Electronics 9, Stationery 9, Personal Care 10) |
| Total stock value | PKR 1,162,496 |
| Low-stock items | 8 |
| Out-of-stock items | 3 |
| Items on the Reorder List | 11 |
| Reorder List order cost (at suggested quantities) | PKR 191,760 |
| Top category by stock value | Electronics, PKR 415,589 (35.7%) |
| Top SKU by stock value | EL-004 Bluetooth Earbuds, PKR 162,191 |
| Lowest / highest margin | Cooking Oil 5L, 15.2% / USB Cable 1m, 31.3% |
| Sample movements | 30 (Oct 2026, log only) |
| Checks | 35 passing (`python3 src/checks.py`) |

Verification: `python3 src/checks.py` (35 checks pass) plus an
independent reopen of the workbook — 4 sheets in order (Dashboard,
Inventory, Reorder List, Movements), Inventory table `InventoryData`
A1:N49, live formulas in Inventory L/M/N, Dashboard B5–B9 and the
SUMIF category rows, one bar chart on Dashboard, 12 Reorder List
rows including the header.

## How to run it (under 5 steps)

First time only: `pip install -r requirements.txt` (openpyxl 3.1.2,
verified with Python 3.12).

1. Open `outputs/inventory_tracker_SAMPLE.xlsx` — that is the
   deliverable.
2. To regenerate the sample data: `python3 src/generate_sample_data.py`.
3. To rebuild the workbook: `python3 src/build_tracker.py`.
4. To check the data: `python3 src/checks.py`.
5. To reuse it for a real client: replace
   `data/raw/inventory_SAMPLE.csv` with the client's stock list
   (same 11 columns) and re-run step 3 — Dashboard, statuses and
   the Reorder List rebuild themselves from the new lines.

## Tools

- Python 3.12 · openpyxl 3.1.2 (pinned in `requirements.txt`)
- Excel / Google Sheets (the client's tool, not a new tool to learn)

## Data source note

**SAMPLE data, generated 4 Nov 2026.** No real business's stock is
involved. The tracker, the formulas and the workbook structure are
the product; the numbers exist to prove them.
