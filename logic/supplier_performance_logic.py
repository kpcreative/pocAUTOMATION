from logic.base import fetch_df

# How does this supplier perform overall?
def supplier_delivery_snapshot(supplier_id):
    df = fetch_df(
        """
        SELECT
            p.PO_NUMBER,
            COUNT(m.GR_NUMBER) AS GR_COUNT,
            SUM(m.DELIVERED_QTY) AS TOTAL_DELIVERED
        FROM zpo_header p
        LEFT JOIN zmatdoc_flight m
        ON p.PO_NUMBER = m.PO_NUMBER
        WHERE p.SUPPLIER_ID = ?
        GROUP BY p.PO_NUMBER
        """,
        [supplier_id]
    )

    return df
