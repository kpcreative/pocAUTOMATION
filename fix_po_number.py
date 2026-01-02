import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "sap_mm_ai.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("Before update:")
cursor.execute("SELECT PO_NUMBER FROM zpo_header")
for row in cursor.fetchall():
    print(row[0])

# SAFE UPDATE: remove extra 0 after '45'
cursor.execute("""
UPDATE zpo_header
SET PO_NUMBER =
    SUBSTR(PO_NUMBER, 1, 2) || SUBSTR(PO_NUMBER, 4)
WHERE LENGTH(PO_NUMBER) = 10
  AND SUBSTR(PO_NUMBER, 3, 1) = '0'
""")

conn.commit()

print("\nAfter update:")
cursor.execute("SELECT PO_NUMBER FROM zpo_header")
for row in cursor.fetchall():
    print(row[0])

conn.close()
print("\n✅ PO_NUMBER correction completed successfully")
