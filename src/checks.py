"""Checks as code for P8. Recomputes every headline number from the raw CSV
and verifies the workbook structure (live formulas, table, chart, sheets).
openpyxl does not calculate formulas, so formula cells are asserted by
their formula strings, never by cached values."""
import csv
import sys
from pathlib import Path
from openpyxl import load_workbook

BASE = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader(open(BASE / "data" / "raw" / "inventory_SAMPLE.csv")))
fails = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f" — {detail}" if detail else ""))
    if not cond:
        fails.append(name)


def stock(r):
    return int(r["Stock on Hand"])


def rp(r):
    return int(r["Reorder Point"])


total_value = sum(stock(r) * int(r["Unit Cost (PKR)"]) for r in rows)
low = [r for r in rows if 0 < stock(r) < rp(r)]
out = [r for r in rows if stock(r) == 0]
reorder = [r for r in rows if stock(r) < rp(r)]
cats = sorted({r["Category"] for r in rows})
cat_val = {c: sum(stock(r) * int(r["Unit Cost (PKR)"]) for r in rows
                if r["Category"] == c) for c in cats}

check("SKU count = 48", len(rows) == 48, str(len(rows)))
check("categories = 5", len(cats) == 5, str(cats))
check("no duplicate SKUs", len({r["SKU"] for r in rows}) == 48)
check("no negative stock or cost",
      all(stock(r) >= 0 and int(r["Unit Cost (PKR)"]) > 0 for r in rows))
check("selling price above cost for every SKU",
      all(int(r["Selling Price (PKR)"]) > int(r["Unit Cost (PKR)"]) for r in rows))
check("total stock value = 1,162,496", total_value == 1162496, str(total_value))
check("low-stock count = 8", len(low) == 8, str([r["SKU"] for r in low]))
check("out-of-stock count = 3", len(out) == 3, str([r["SKU"] for r in out]))
check("reorder-list size = 11", len(reorder) == 11)
check("category values sum to total", sum(cat_val.values()) == total_value)
check("Electronics is the top category by stock value",
      max(cat_val, key=cat_val.get) == "Electronics", str(cat_val))
check("reorder order cost = 191,760",
      sum((rp(r) * 2 - stock(r)) * int(r["Unit Cost (PKR)"]) for r in reorder) == 191760)

wb = load_workbook(BASE / "outputs" / "inventory_tracker_SAMPLE.xlsx")
check("sheets = Dashboard, Inventory, Reorder List, Movements",
      wb.sheetnames == ["Dashboard", "Inventory", "Reorder List", "Movements"],
      str(wb.sheetnames))
inv = wb["Inventory"]
check("Inventory rows = 49 incl header", inv.max_row == 49, str(inv.max_row))
check("Inventory has an Excel Table",
      len(inv.tables) == 1 and "InventoryData" in inv.tables)
check("Stock Value col is a live formula (row 2)",
      inv["L2"].value == "=H2*F2", str(inv["L2"].value))
check("Margin % col is a live formula (row 2)",
      isinstance(inv["M2"].value, str) and "(G2-F2)/G2" in inv["M2"].value,
      str(inv["M2"].value))
check("Status col is a live formula (row 2)",
      isinstance(inv["N2"].value, str) and "OUT OF STOCK" in inv["N2"].value
      and "LOW STOCK" in inv["N2"].value, str(inv["N2"].value))
check("Status formula covers all 48 rows",
      all(isinstance(inv[f"N{i}"].value, str) and inv[f"N{i}"].value.startswith("=IF")
          for i in range(2, 50)))
d = wb["Dashboard"]
check("Dashboard total SKUs is a COUNTA formula",
      d["B5"].value == "=COUNTA(Inventory!A2:A49)", str(d["B5"].value))
check("Dashboard stock value is a SUM formula",
      d["B6"].value == "=SUM(Inventory!L2:L49)", str(d["B6"].value))
check("Dashboard low count is a COUNTIF formula",
      d["B7"].value == '=COUNTIF(Inventory!N2:N49,"LOW STOCK")', str(d["B7"].value))
check("Dashboard out count is a COUNTIF formula",
      d["B8"].value == '=COUNTIF(Inventory!N2:N49,"OUT OF STOCK")', str(d["B8"].value))
check("Dashboard reorder count = low + out",
      d["B9"].value == "=B7+B8", str(d["B9"].value))
check("Dashboard category rows are SUMIF formulas",
      all(isinstance(d[f"B{i}"].value, str) and "SUMIF" in d[f"B{i}"].value
          for i in range(14, 19)))
check("Dashboard has a bar chart", len(d._charts) >= 1)
rl = wb["Reorder List"]
check("Reorder List rows = 12 incl header (11 items)",
      rl.max_row == 12, str(rl.max_row))
check("Reorder List Suggested Qty is RP*2 - Stock (row 2)",
      rl["H2"].value == "=G2*2-F2", str(rl["H2"].value))
check("Reorder List Order Cost is Qty x Cost (row 2)",
      rl["I2"].value == "=H2*E2", str(rl["I2"].value))
check("Reorder List row 2 links to first LOW item (GR-002, Inventory row 3)",
      rl["A2"].value == "=Inventory!A3", str(rl["A2"].value))
check("every Reorder List row links back to Inventory",
      all(isinstance(rl[f"A{i}"].value, str)
          and rl[f"A{i}"].value.startswith("=Inventory!A")
          for i in range(2, 13)))
mv = wb["Movements"]
check("Movements rows = 32 (note + header + 30)",
      mv.max_row == 32, str(mv.max_row))
check("Movements effect col is a live IN/OUT formula",
      isinstance(mv["F3"].value, str) and 'IF(D3="IN"' in mv["F3"].value,
      str(mv["F3"].value))
check("Movements header states no live running balance",
      "no live running balance" in str(mv["A1"].value).lower())
print(f"\n{len(fails)} failures" if fails else "\nALL CHECKS PASS")
sys.exit(1 if fails else 0)
