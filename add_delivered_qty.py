import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "sap_mm_ai.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 1. Add column if not exists
try:
    cur.execute("ALTER TABLE zmatdoc_flight ADD COLUMN DELIVERED_QTY INTEGER")
    print("✅ DELIVERED_QTY column added")
except sqlite3.OperationalError:
    print("ℹ️ DELIVERED_QTY column already exists")

# 2. Populate delivered quantity = 1 per row (POC logic)
cur.execute("""
UPDATE zmatdoc_flight
SET DELIVERED_QTY = 1
WHERE DELIVERED_QTY IS NULL
""")

conn.commit()
conn.close()

print("✅ Delivered quantity populated successfully")
