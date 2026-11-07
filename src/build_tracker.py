"""Build the P8 inventory tracker workbook from data/raw/inventory_SAMPLE.csv.

Inventory sheet = the 48 SAMPLE SKUs as an Excel Table, with live-formula
columns: Stock Value (= Stock x Cost), Margin % (= (Price - Cost) / Price)
and Status (= OUT OF STOCK / LOW STOCK / OK from Stock vs Reorder Point).
Dashboard KPIs are live formulas (COUNTA / SUM / COUNTIF) over Inventory,
plus a stock-value-by-category table (SUMIF) and a native bar chart.
Reorder List holds only the LOW/OUT items, every cell linked back to its
Inventory row, with Suggested Order Qty = Reorder Point x 2 - Stock on Hand
and Order Cost = Suggested Qty x Unit Cost, both live formulas.
Movements is a 30-row SAMPLE log for Oct 2026 (deterministic, seed 42);
it is a log only — it does NOT feed back into Inventory stock levels and
there is no live running balance, stated honestly on the sheet itself.
"""
import csv
import random
from pathlib import Path
from openpyxl import Workbook
from openpyxl.worksheet.table import Table
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Font

BASE = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader(open(BASE / "data" / "raw" / "inventory_SAMPLE.csv")))
N = len(rows)
LAST = N + 1  # last Inventory data row (row 1 = header)

wb = Workbook()
ws = wb.active
ws.title = "Inventory"
headers = ["SKU", "Product", "Category", "Supplier", "Unit",
           "Unit Cost (PKR)", "Selling Price (PKR)", "Stock on Hand",
           "Reorder Point", "Reorder Qty", "Lead Time Days",
           "Stock Value (PKR)", "Margin %", "Status"]
ws.append(headers)
for i, r in enumerate(rows, 2):
    ws.append([r["SKU"], r["Product"], r["Category"], r["Supplier"], r["Unit"],
               int(r["Unit Cost (PKR)"]), int(r["Selling Price (PKR)"]),
               int(r["Stock on Hand"]), int(r["Reorder Point"]),
               int(r["Reorder Qty"]), int(r["Lead Time Days"]),
               f"=H{i}*F{i}", f"=IF(G{i}=0,0,(G{i}-F{i})/G{i})",
               f'=IF(H{i}=0,"OUT OF STOCK",IF(H{i}<I{i},"LOW STOCK","OK"))'])
ws.add_table(Table(displayName="InventoryData", ref=f"A1:N{LAST}"))
for c in ws[1]:
    c.font = Font(bold=True)
for col, w in zip("ABCDEFGHIJKLMN", [9, 26, 14, 24, 8, 15, 17, 14, 13, 12, 14, 17, 10, 14]):
    ws.column_dimensions[col].width = w
for i in range(2, LAST + 1):
    for col in ("F", "G", "L"):
        ws[f"{col}{i}"].number_format = "#,##0"
    ws[f"M{i}"].number_format = "0.0%"

# Dashboard
d = wb.create_sheet("Dashboard")
d["A1"] = "Inventory & Stock Tracker — PakStore (SAMPLE)"
d["A1"].font = Font(bold=True, size=14)
d["A2"] = ("Live formulas over the Inventory sheet — change a stock level "
           "there and this page, and the Reorder List, update themselves.")
d["A4"] = "KPI"; d["B4"] = "Value"; d["C4"] = "How it is calculated (live formula)"
for c in d[4]:
    c.font = Font(bold=True)
d["A5"] = "Total SKUs"; d["B5"] = f"=COUNTA(Inventory!A2:A{LAST})"
d["A6"] = "Total stock value (PKR)"; d["B6"] = f"=SUM(Inventory!L2:L{LAST})"
d["B6"].number_format = "#,##0"
d["A7"] = "Low-stock items"; d["B7"] = f'=COUNTIF(Inventory!N2:N{LAST},"LOW STOCK")'
d["A8"] = "Out-of-stock items"; d["B8"] = f'=COUNTIF(Inventory!N2:N{LAST},"OUT OF STOCK")'
d["A9"] = "Items on the Reorder List"; d["B9"] = "=B7+B8"
cats = sorted({r["Category"] for r in rows})
d["A10"] = "Categories tracked"; d["B10"] = f"=COUNTA(A14:A{13 + len(cats)})"
d["A12"] = "Stock value by category (PKR)"; d["A12"].font = Font(bold=True)
d["A13"] = "Category"; d["B13"] = "Stock Value (PKR)"; d["C13"] = "Share"
for c in d[13]:
    c.font = Font(bold=True)
for i, cat in enumerate(cats):
    row = 14 + i
    d[f"A{row}"] = cat
    d[f"B{row}"] = (f"=SUMIF(Inventory!$C$2:$C${LAST},A{row},"
                    f"Inventory!$L$2:$L${LAST})")
    d[f"B{row}"].number_format = "#,##0"
    d[f"C{row}"] = f"=IF($B$6=0,0,B{row}/$B$6)"
    d[f"C{row}"].number_format = "0.0%"
bar = BarChart()
bar.title = "Stock value by category (PKR)"
bar.y_axis.title = "PKR"; bar.x_axis.title = "Category"
bar.add_data(Reference(d, min_col=2, min_row=13, max_row=13 + len(cats)),
             titles_from_data=True)
bar.set_categories(Reference(d, min_col=1, min_row=14, max_row=13 + len(cats)))
bar.height = 7; bar.width = 13
d.add_chart(bar, "A20")
d.column_dimensions["A"].width = 42
d.column_dimensions["B"].width = 20
d.column_dimensions["C"].width = 30

# Reorder List: only LOW / OUT items, every cell linked to its Inventory row
rl = wb.create_sheet("Reorder List")
rl.append(["SKU", "Product", "Category", "Supplier", "Unit Cost (PKR)",
           "Stock on Hand", "Reorder Point", "Suggested Order Qty",
           "Order Cost (PKR)"])
for c in rl[1]:
    c.font = Font(bold=True)
out_row = 2
for i, r in enumerate(rows, 2):
    stock, rp = int(r["Stock on Hand"]), int(r["Reorder Point"])
    if stock >= rp:
        continue
    rl[f"A{out_row}"] = f"=Inventory!A{i}"
    rl[f"B{out_row}"] = f"=Inventory!B{i}"
    rl[f"C{out_row}"] = f"=Inventory!C{i}"
    rl[f"D{out_row}"] = f"=Inventory!D{i}"
    rl[f"E{out_row}"] = f"=Inventory!F{i}"
    rl[f"F{out_row}"] = f"=Inventory!H{i}"
    rl[f"G{out_row}"] = f"=Inventory!I{i}"
    rl[f"H{out_row}"] = f"=G{out_row}*2-F{out_row}"
    rl[f"I{out_row}"] = f"=H{out_row}*E{out_row}"
    rl[f"E{out_row}"].number_format = "#,##0"
    rl[f"I{out_row}"].number_format = "#,##0"
    out_row += 1
for col, w in zip("ABCDEFGHI", [9, 26, 14, 24, 15, 14, 13, 19, 16]):
    rl.column_dimensions[col].width = w

# Movements: 30-row SAMPLE log, Oct 2026, deterministic seed 42
mv = wb.create_sheet("Movements")
mv["A1"] = ("SAMPLE stock movements, Oct 2026 — a LOG ONLY: these rows do "
            "NOT change Inventory stock levels; there is no live running "
            "balance on this sheet.")
mv["A1"].font = Font(bold=True)
mv.append(["Date", "SKU", "Product", "Movement", "Qty", "Stock effect", "Note"])
for c in mv[2]:
    c.font = Font(bold=True)
rng = random.Random(42)
for i in range(30):
    r = rng.choice(rows)
    day = rng.randint(1, 31)
    move = rng.choice(["IN", "IN", "OUT"])
    qty = rng.randint(1, 30)
    note = ("Supplier delivery" if move == "IN"
            else rng.choice(["Shop sale", "Shop sale", "Damaged stock written off"]))
    row = 3 + i
    mv[f"A{row}"] = f"2026-10-{day:02d}"
    mv[f"B{row}"] = r["SKU"]
    mv[f"C{row}"] = r["Product"]
    mv[f"D{row}"] = move
    mv[f"E{row}"] = qty
    mv[f"F{row}"] = f'=IF(D{row}="IN",E{row},-E{row})'
    mv[f"G{row}"] = note
for col, w in zip("ABCDEFG", [12, 9, 26, 10, 6, 13, 30]):
    mv.column_dimensions[col].width = w

wb.move_sheet("Dashboard", offset=-1)  # Dashboard first, as the task order requires
wb.save(BASE / "outputs" / "inventory_tracker_SAMPLE.xlsx")
print(f"saved workbook: {N} SKUs, reorder list rows {out_row - 2}, "
      f"30 movements, sheets {wb.sheetnames}")
