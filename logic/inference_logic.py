from logic.base import fetch_df
from logic.text_normalizer import normalize_text


# answers---Supplier X provided which services on date D?
def find_services_by_supplier_and_date(supplier_id, service_text, service_date):
    service_key = normalize_text(service_text)

    df = fetch_df(
        """
        SELECT *
        FROM zmatdoc_flight
        WHERE SUPPLIER_ID = ?
          AND FLIGHT_DATE = ?
        """,
        [supplier_id, service_date]
    )

    results = []

    for _, row in df.iterrows():
        desc_key = normalize_text(row["DESCRIPTION"])
        if service_key in desc_key:
            results.append(row)

    return results


# 📌 Answers:

# “Supplier X provided jet fuel on this date → which PO?”
def get_po_numbers_for_supplier_service_date(supplier_id, service_text, service_date):
    rows = find_services_by_supplier_and_date(
        supplier_id, service_text, service_date
    )

    po_numbers = {row["PO_NUMBER"] for row in rows}
    return list(po_numbers)

# answers-- “Supplier X provided jet fuel on this date → which GR?”
def get_gr_numbers_for_supplier_service_date(supplier_id, service_text, service_date):
    rows = find_services_by_supplier_and_date(
        supplier_id, service_text, service_date
    )

    gr_numbers = {row["GR_NUMBER"] for row in rows if row["GR_NUMBER"]}
    return list(gr_numbers)


# answers-- “For PO 450000005, where service provided is jet fuel, what is the delivery timeline?  i.e date--”
def get_service_delivery_timeline(po_number, service_text):
    service_key = normalize_text(service_text)

    df = fetch_df(
        """
        SELECT FLIGHT_DATE, DELIVERED_QTY, DESCRIPTION
        FROM zmatdoc_flight
        WHERE PO_NUMBER = ?
        ORDER BY FLIGHT_DATE
        """,
        [po_number]
    )

    timeline = []

    for _, row in df.iterrows():
        if service_key in normalize_text(row["DESCRIPTION"]):
            timeline.append({
                "DATE": row["FLIGHT_DATE"],
                "QTY": row["DELIVERED_QTY"],
                "DESCRIPTION": row["DESCRIPTION"]
            })

    return timeline


# answers-- “For PO 450000005, where service provided is jet fuel on date D, what is the GR number..vo v exact ?”
def get_gr_for_po_service_date(po_number, service_text, service_date):
    service_key = normalize_text(service_text)

    df = fetch_df(
        """
        SELECT *
        FROM zmatdoc_flight
        WHERE PO_NUMBER = ?
          AND FLIGHT_DATE = ?
        """,
        [po_number, service_date]
    )

    for _, row in df.iterrows():
        if service_key in normalize_text(row["DESCRIPTION"]):
            return row["GR_NUMBER"]

    return None
