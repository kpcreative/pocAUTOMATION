from logic.base import fetch_df

# overhow many days this po was delivered
def get_delivery_summary(po_number):
    df = fetch_df(
        """
        SELECT
            MIN(FLIGHT_DATE) AS FIRST_DELIVERY,
            MAX(FLIGHT_DATE) AS LAST_DELIVERY,
            COUNT(DISTINCT FLIGHT_DATE) AS DELIVERY_DAYS
        FROM zmatdoc_flight
        WHERE PO_NUMBER = ?
        """,
        [po_number]
    )

    return df.iloc[0].to_dict() if not df.empty else {}
