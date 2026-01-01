from logic.base import fetch_df
from decimal import Decimal
from logic.text_normalizer import normalize_text

# ---------- ORDERED QUANTITY (PO ITEM LEVEL) ----------
def get_ordered_quantities(po_number):
    """
    Returns ordered quantity per PO_ITEM
    """
    return fetch_df(
        """
        SELECT PO_ITEM, MATERIAL, QUANTITY
        FROM zpo_item
        WHERE PO_NUMBER = ?
        """,
        [po_number]
    )


# ---------- DELIVERED QUANTITY (FROM MATERIAL DOCS) ----------
def get_delivered_quantities(po_number):
    """
    Returns delivered quantity per service description
    """
    return fetch_df(
        """
        SELECT DESCRIPTION, SUM(DELIVERED_QTY) AS DELIVERED_QTY
        FROM zmatdoc_flight
        WHERE PO_NUMBER = ?
        GROUP BY DESCRIPTION
        """,
        [po_number]
    )


# ---------- DELIVERY STATUS (QUANTITY-BASED) ----------
def get_delivery_status(po_number):
    ordered_df = get_ordered_quantities(po_number)
    delivered_df = get_delivered_quantities(po_number)

    if ordered_df.empty:
        return {"error": "PO not found"}

    ordered_qty = ordered_df["QUANTITY"].sum()
    delivered_qty = (
        delivered_df["DELIVERED_QTY"].sum()
        if not delivered_df.empty
        else 0
    )

    pending_qty = ordered_qty - delivered_qty

    if delivered_qty == 0:
        status = "NOT DELIVERED"
    elif delivered_qty < ordered_qty:
        status = "PARTIALLY DELIVERED"
    elif delivered_qty == ordered_qty:
        status = "FULLY DELIVERED"
    else:
        status = "OVER DELIVERED"

    return {
        "PO_NUMBER": po_number,
        "ORDERED_QTY": ordered_qty,
        "DELIVERED_QTY": delivered_qty,
        "PENDING_QTY": pending_qty,
        "STATUS": status
    }


# ---------- VALUE RECONCILIATION ----------
def get_value_reconciliation(po_number):
    po_df = fetch_df(
        "SELECT PO_AMOUNT FROM zpo_header WHERE PO_NUMBER = ?",
        [po_number]
    )

    gr_df = fetch_df(
        "SELECT GR_AMOUNT FROM zgr_header WHERE PO_NUMBER = ?",
        [po_number]
    )

    if po_df.empty:
        return {"error": "PO not found"}

    po_amount = Decimal(po_df.iloc[0]["PO_AMOUNT"])
    gr_amount = (
        gr_df["GR_AMOUNT"].apply(Decimal).sum()
        if not gr_df.empty
        else Decimal("0")
    )

    return {
        "PO_VALUE": po_amount,
        "GR_VALUE": gr_amount,
        "PENDING_VALUE": po_amount - gr_amount
    }


# ---------- FINAL MASTER RECONCILIATION ----------
def full_po_reconciliation(po_number):
    qty_status = get_delivery_status(po_number)
    value_status = get_value_reconciliation(po_number)

    if "error" in qty_status:
        return qty_status

    return {
        "PO_NUMBER": po_number,
        "DELIVERY_STATUS": qty_status["STATUS"],
        "ORDERED_QTY": qty_status["ORDERED_QTY"],
        "DELIVERED_QTY": qty_status["DELIVERED_QTY"],
        "PENDING_QTY": qty_status["PENDING_QTY"],
        "PO_VALUE": value_status["PO_VALUE"],
        "GR_VALUE": value_status["GR_VALUE"],
        "PENDING_VALUE": value_status["PENDING_VALUE"]
    }





# reconcilliation on based of service--
# For PO 450000005, where service provided is jet fuel, what is the reconciliation?


def get_ordered_qty_for_service(po_number, service_text):
    service_key = normalize_text(service_text)

    df = fetch_df(
        """
        SELECT MATERIAL, QUANTITY
        FROM zpo_item
        WHERE PO_NUMBER = ?
        """,
        [po_number]
    )

    total_qty = 0

    for _, row in df.iterrows():
        material_key = normalize_text(row["MATERIAL"])

        # semantic containment match harmonious
        if service_key in material_key or material_key in service_key:
            total_qty += row["QUANTITY"]

    return total_qty


def get_delivered_qty_for_service(po_number, service_text):
    service_key = normalize_text(service_text)

    df = fetch_df(
        """
        SELECT DESCRIPTION, DELIVERED_QTY
        FROM zmatdoc_flight
        WHERE PO_NUMBER = ?
        """,
        [po_number]
    )

    total_qty = 0

    for _, row in df.iterrows():
        desc_key = normalize_text(row["DESCRIPTION"])

        if service_key in desc_key:
            total_qty += row["DELIVERED_QTY"]

    return total_qty

def reconcile_po_by_service(po_number, service_text):
    ordered_qty = get_ordered_qty_for_service(po_number, service_text)
    delivered_qty = get_delivered_qty_for_service(po_number, service_text)

    pending_qty = ordered_qty - delivered_qty

    if delivered_qty == 0:
        status = "NOT DELIVERED"
    elif delivered_qty < ordered_qty:
        status = "PARTIALLY DELIVERED"
    elif delivered_qty == ordered_qty:
        status = "FULLY DELIVERED"
    else:
        status = "OVER DELIVERED"

    return {
        "PO_NUMBER": po_number,
        "SERVICE": service_text.upper(),
        "ORDERED_QTY": ordered_qty,
        "DELIVERED_QTY": delivered_qty,
        "PENDING_QTY": pending_qty,
        "STATUS": status
    }
