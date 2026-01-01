from logic.po_logic import get_po_by_number
from logic.gr_logic import get_total_gr_amount_by_po
from decimal import Decimal

def po_gr_reconciliation(po_number):
    po_df = get_po_by_number(po_number)

    if po_df.empty:
        return {"error": "PO not found"}

    po_amount = Decimal(po_df.iloc[0]["PO_AMOUNT"])
    gr_amount = get_total_gr_amount_by_po(po_number)

    return {
        "PO_NUMBER": po_number,
        "PO_AMOUNT": po_amount,
        "GR_AMOUNT": gr_amount,
        "DIFFERENCE": po_amount - gr_amount
    }
