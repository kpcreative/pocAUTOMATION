from logic.base import fetch_df

# Is anything delivered that was not ordered?
def find_service_exceptions(po_number):
    """
    Detects over-delivery and unplanned delivery
    """
    po_items = fetch_df(
        "SELECT MATERIAL FROM zpo_item WHERE PO_NUMBER = ?",
        [po_number]
    )

    delivered = fetch_df(
        "SELECT DESCRIPTION FROM zmatdoc_flight WHERE PO_NUMBER = ?",
        [po_number]
    )

    po_materials = set(po_items["MATERIAL"])
    delivered_services = set(delivered["DESCRIPTION"])

    unplanned = delivered_services - po_materials

    return {
        "UNPLANNED_SERVICES": list(unplanned)
    }
