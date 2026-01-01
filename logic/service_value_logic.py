from logic.base import fetch_df
from logic.text_normalizer import normalize_text
from decimal import Decimal


# How much value has been delivered for jet fuel under this PO
def get_delivered_amount_for_service(po_number, service_text):
    service_key = normalize_text(service_text)

    df = fetch_df(
        """
        SELECT DESCRIPTION, AMOUNT
        FROM zmatdoc_flight
        WHERE PO_NUMBER = ?
        """,
        [po_number]
    )

    total_amount = Decimal("0")

    for _, row in df.iterrows():
        desc_key = normalize_text(row["DESCRIPTION"])
        if service_key in desc_key:
            total_amount += Decimal(row["AMOUNT"])

    return total_amount



# “What was the ordered value for jet fuel in this PO?”
def get_ordered_amount_for_service(po_number, service_text):
    from logic.reconciliation_logic import get_ordered_qty_for_service

    po_df = fetch_df(
        "SELECT PO_AMOUNT FROM zpo_header WHERE PO_NUMBER = ?",
        [po_number]
    )

    if po_df.empty:
        return Decimal("0")

    po_amount = Decimal(po_df.iloc[0]["PO_AMOUNT"])

    # quantities
    total_qty_df = fetch_df(
        "SELECT SUM(QUANTITY) AS TOTAL_QTY FROM zpo_item WHERE PO_NUMBER = ?",
        [po_number]
    )

    total_qty = total_qty_df.iloc[0]["TOTAL_QTY"]
    if not total_qty:
        return Decimal("0")

    service_qty = get_ordered_qty_for_service(po_number, service_text)

    ratio = Decimal(service_qty) / Decimal(total_qty)
    return po_amount * ratio

# For this PO, for jet fuel, what is the amount?
def reconcile_service_amount(po_number, service_text):
    ordered_amount = get_ordered_amount_for_service(po_number, service_text)
    delivered_amount = get_delivered_amount_for_service(po_number, service_text)

    pending_amount = ordered_amount - delivered_amount

    if delivered_amount == 0:
        status = "NOT BILLED"
    elif delivered_amount < ordered_amount:
        status = "PARTIALLY BILLED"
    elif delivered_amount == ordered_amount:
        status = "FULLY BILLED"
    else:
        status = "OVER BILLED"

    return {
        "PO_NUMBER": po_number,
        "SERVICE": service_text.upper(),
        "ORDERED_AMOUNT": ordered_amount,
        "DELIVERED_AMOUNT": delivered_amount,
        "PENDING_AMOUNT": pending_amount,
        "STATUS": status
    }
