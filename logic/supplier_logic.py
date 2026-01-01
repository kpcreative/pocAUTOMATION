from logic.base import fetch_df

def get_supplier_by_id(supplier_id):
    return fetch_df(
        "SELECT * FROM zsupplier WHERE SUPPLIER_ID = ?",
        [supplier_id]
    )

def get_all_suppliers():
    return fetch_df("SELECT * FROM zsupplier")

def get_suppliers_with_pos():
    return fetch_df("""
        SELECT DISTINCT s.*
        FROM zsupplier s
        JOIN zpo_header p ON s.SUPPLIER_ID = p.SUPPLIER_ID
    """)
