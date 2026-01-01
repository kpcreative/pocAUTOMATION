from logic.base import fetch_df
from decimal import Decimal

def get_grs_by_po(po_number):
    return fetch_df(
        "SELECT * FROM zgr_header WHERE PO_NUMBER = ?",
        [po_number]
    )

def get_total_gr_amount_by_po(po_number):
    df = fetch_df(
        "SELECT GR_AMOUNT FROM zgr_header WHERE PO_NUMBER = ?",
        [po_number]
    )
    df["GR_AMOUNT"] = df["GR_AMOUNT"].apply(Decimal)
    return df["GR_AMOUNT"].sum()
