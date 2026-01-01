from logic.base import fetch_df
from decimal import Decimal

def get_po_by_number(po_number):
    return fetch_df(
        "SELECT * FROM zpo_header WHERE PO_NUMBER = ?",
        [po_number]
    )

def get_pos_by_supplier(supplier_id):
    return fetch_df(
        "SELECT * FROM zpo_header WHERE SUPPLIER_ID = ?",
        [supplier_id]
    )

def get_total_po_amount_by_supplier(supplier_id):
    df = fetch_df(
        "SELECT PO_AMOUNT FROM zpo_header WHERE SUPPLIER_ID = ?",
        [supplier_id]
    )
    df["PO_AMOUNT"] = df["PO_AMOUNT"].apply(Decimal)
    return df["PO_AMOUNT"].sum()

def get_supplier_by_po(po_number):
    """
    Returns supplier details for a given PO number
    """
    return fetch_df(
        """
        SELECT s.*
        FROM zpo_header p
        JOIN zsupplier s
        ON p.SUPPLIER_ID = s.SUPPLIER_ID
        WHERE p.PO_NUMBER = ?
        """,
        [po_number]
    )
