from logic.base import fetch_df

# Is there GR without PO?
def find_orphan_grs():
    """
    GR exists but PO missing
    """
    return fetch_df(
        """
        SELECT g.*
        FROM zgr_header g
        LEFT JOIN zpo_header p
        ON g.PO_NUMBER = p.PO_NUMBER
        WHERE p.PO_NUMBER IS NULL
        """
    )
