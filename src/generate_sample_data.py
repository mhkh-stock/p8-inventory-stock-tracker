"""Generate the P8 SAMPLE inventory CSV for fictional shop "PakStore".

Deterministic: seed 42 — re-running reproduces the identical CSV.
48 SKUs across 5 categories. A few SKUs are forced OUT OF STOCK
(stock = 0) and a few LOW STOCK (stock below reorder point) so the
Reorder List sheet has real content to show; every other SKU is
deliberately stocked at or above its reorder point.

Columns: SKU, Product, Category, Supplier, Unit, Unit Cost (PKR),
Selling Price (PKR), Stock on Hand, Reorder Point, Reorder Qty,
Lead Time Days.
"""
import csv
import random
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "data" / "raw" / "inventory_SAMPLE.csv"

# (product, unit, cost_low, cost_high, markup)
CATALOG = {
    "Groceries": (
        ["Shan Foods Distributors", "Metro Wholesale Lahore"],
        [
            ("Basmati Rice 5kg", "bag", 1400, 1600, 1.22),
            ("Cooking Oil 5L", "bottle", 2400, 2700, 1.18),
            ("Sugar 5kg", "bag", 650, 750, 1.20),
            ("Wheat Flour 10kg", "bag", 1100, 1250, 1.18),
            ("Tea Leaves 500g", "pack", 700, 850, 1.30),
            ("Lentils (Daal) 2kg", "pack", 480, 560, 1.25),
            ("Spice Mix 200g", "pack", 220, 300, 1.40),
            ("Salt 1kg", "pack", 90, 120, 1.35),
            ("Pasta 500g", "pack", 260, 320, 1.30),
            ("Canned Tomatoes 400g", "tin", 180, 240, 1.35),
        ],
    ),
    "Household": (
        ["Habib Traders", "Karachi Goods Co."],
        [
            ("Washing Powder 3kg", "pack", 900, 1050, 1.22),
            ("Dishwashing Liquid 1L", "bottle", 380, 460, 1.30),
            ("Floor Cleaner 2L", "bottle", 420, 500, 1.28),
            ("Tissue Box (200 sheets)", "box", 210, 270, 1.30),
            ("Garbage Bags (30 pcs)", "roll", 300, 360, 1.28),
            ("Broom", "piece", 250, 320, 1.35),
            ("Mop Set", "set", 700, 850, 1.25),
            ("Air Freshener Spray", "can", 340, 420, 1.32),
            ("Laundry Bar Soap (4 pcs)", "pack", 280, 340, 1.25),
            ("Scrub Sponge (6 pcs)", "pack", 150, 200, 1.35),
        ],
    ),
    "Electronics": (
        ["TechLink Distributors", "Al-Fatah Electronics"],
        [
            ("USB Cable 1m", "piece", 250, 350, 1.45),
            ("Phone Charger 18W", "piece", 900, 1200, 1.35),
            ("Wireless Mouse", "piece", 1100, 1400, 1.30),
            ("Bluetooth Earbuds", "piece", 2200, 2800, 1.28),
            ("LED Bulb 12W (4 pcs)", "pack", 600, 750, 1.30),
            ("Power Strip 4-Socket", "piece", 800, 1000, 1.30),
            ("AA Batteries (8 pcs)", "pack", 320, 400, 1.35),
            ("HDMI Cable 2m", "piece", 550, 700, 1.35),
            ("Mobile Stand", "piece", 450, 600, 1.40),
        ],
    ),
    "Stationery": (
        ["PaperLine Supplies", "City Stationers"],
        [
            ("A4 Notebook (3 pcs)", "pack", 380, 460, 1.30),
            ("Ballpoint Pen (10 pcs)", "pack", 220, 280, 1.35),
            ("Geometry Box", "piece", 300, 380, 1.30),
            ("A4 Paper Ream", "ream", 650, 780, 1.22),
            ("Highlighter Set (4 pcs)", "set", 340, 420, 1.32),
            ("Stapler + Pins", "set", 400, 500, 1.30),
            ("Glue Stick (3 pcs)", "pack", 180, 240, 1.35),
            ("File Folder (5 pcs)", "pack", 260, 330, 1.30),
            ("Colour Pencils (12 pcs)", "pack", 290, 360, 1.32),
        ],
    ),
    "Personal Care": (
        ["DermaCare Distributors", "GlowMart Supplies"],
        [
            ("Shampoo 400ml", "bottle", 550, 680, 1.28),
            ("Bathing Soap (3 pcs)", "pack", 330, 420, 1.30),
            ("Toothpaste 140g", "tube", 280, 350, 1.30),
            ("Face Wash 100ml", "tube", 480, 600, 1.32),
            ("Hair Oil 200ml", "bottle", 380, 470, 1.30),
            ("Body Lotion 250ml", "bottle", 520, 650, 1.28),
            ("Deodorant Spray", "can", 420, 520, 1.30),
            ("Hand Wash 500ml", "bottle", 360, 440, 1.30),
            ("Talcum Powder 200g", "bottle", 300, 380, 1.30),
            ("Cotton Pads (80 pcs)", "pack", 200, 260, 1.35),
        ],
    ),
}
PREFIX = {"Groceries": "GR", "Household": "HH", "Electronics": "EL",
          "Stationery": "ST", "Personal Care": "PC"}
# 0-based row indices forced into each status (after catalogue order).
FORCE_OUT = {4, 19, 37}
FORCE_LOW = {1, 8, 13, 22, 26, 31, 40, 45}


def main():
    rng = random.Random(42)
    rows = []
    idx = 0
    for category, (suppliers, products) in CATALOG.items():
        for n, (name, unit, lo, hi, markup) in enumerate(products, 1):
            cost = rng.randint(lo, hi)
            price = int(round(cost * markup / 5.0) * 5)
            rp = rng.randint(8, 30)
            if idx in FORCE_OUT:
                stock = 0
            elif idx in FORCE_LOW:
                stock = max(1, rp - rng.randint(1, max(1, rp - 1)))
            else:
                stock = rp + rng.randint(0, 80)
            rows.append({
                "SKU": f"{PREFIX[category]}-{n:03d}",
                "Product": name,
                "Category": category,
                "Supplier": rng.choice(suppliers),
                "Unit": unit,
                "Unit Cost (PKR)": cost,
                "Selling Price (PKR)": price,
                "Stock on Hand": stock,
                "Reorder Point": rp,
                "Reorder Qty": rng.randint(20, 60),
                "Lead Time Days": rng.randint(3, 14),
            })
            idx += 1
    assert len(rows) == 48, len(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT}: {len(rows)} SKUs, "
          f"{sum(1 for r in rows if r['Stock on Hand'] == 0)} out, "
          f"{sum(1 for r in rows if 0 < r['Stock on Hand'] < r['Reorder Point'])} low")


if __name__ == "__main__":
    main()
