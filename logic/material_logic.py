from logic.base import fetch_df

def get_material_docs_by_po(po_number):
    return fetch_df(
        "SELECT * FROM zmatdoc_flight WHERE PO_NUMBER = ?",
        [po_number]
    )

def get_material_docs_by_flight(flight_no):
    return fetch_df(
        "SELECT * FROM zmatdoc_flight WHERE FLIGHT_NO = ?",
        [flight_no]
    )


