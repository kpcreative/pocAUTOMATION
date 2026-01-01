from logic.base import fetch_df


# Which services of this PO are still pending?
def get_open_services_for_po(po_number):
    """
    Returns services ordered but not fully delivered
    """
    ordered = fetch_df(
        "SELECT MATERIAL, QUANTITY FROM zpo_item WHERE PO_NUMBER = ?",
        [po_number]
    )

    delivered = fetch_df(
        """
        SELECT DESCRIPTION, SUM(DELIVERED_QTY) AS QTY
        FROM zmatdoc_flight
        WHERE PO_NUMBER = ?
        GROUP BY DESCRIPTION
        """,
        [po_number]
    )

    result = []

    for _, row in ordered.iterrows():
        ordered_qty = row["QUANTITY"]
        delivered_qty = delivered["QTY"].sum() if not delivered.empty else 0

        if delivered_qty < ordered_qty:
            result.append({
                "SERVICE": row["MATERIAL"],
                "ORDERED_QTY": ordered_qty,
                "DELIVERED_QTY": delivered_qty,
                "PENDING_QTY": ordered_qty - delivered_qty
            })

    return result
