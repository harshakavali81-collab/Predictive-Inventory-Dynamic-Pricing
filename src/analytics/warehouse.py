"""Local SQLite analytical warehouse. Does not send data over a network."""
from __future__ import annotations
import sqlite3
from pathlib import Path
from src.processing.validation import validate_sales

def export_warehouse(rows: list[dict], db_path: str | Path = "data/generated/inventoryiq.db",
                     schema_path: str | Path = "sql/schema.sql") -> Path:
    validated = validate_sales(rows)
    destination = Path(db_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    schema = Path(schema_path).read_text(encoding="utf-8")
    # Fresh, atomic-ish export: only replace the target if the export has succeeded.
    temp = destination.with_suffix(destination.suffix + ".tmp")
    temp.unlink(missing_ok=True)
    try:
        with sqlite3.connect(temp) as db:
            db.executescript(schema)
            db.executemany(
                "INSERT INTO daily_sales(sale_date,sku,category,units,price,promotion,unit_cost) VALUES(?,?,?,?,?,?,?)",
                [(r["date"],r["sku"],r["category"],r["units"],r["price"],r["promotion"],r["unit_cost"]) for r in validated]
            )
            db.commit()
            count = db.execute("SELECT COUNT(*) FROM daily_sales").fetchone()[0]
            if count != len(validated):
                raise ValueError("Warehouse record count mismatch")
        temp.replace(destination)
    except Exception:
        temp.unlink(missing_ok=True)
        raise
    return destination

def query_kpis(db_path: str | Path = "data/generated/inventoryiq.db") -> list[dict]:
    with sqlite3.connect(db_path) as db:
        db.row_factory = sqlite3.Row
        return [dict(row) for row in db.execute("SELECT * FROM v_sku_kpis ORDER BY sku")]
