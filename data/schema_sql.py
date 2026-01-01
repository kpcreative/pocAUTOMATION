SCHEMA_SQL = {
    "zsupplier": """
        CREATE TABLE IF NOT EXISTS zsupplier (
            MANDT TEXT,
            SUPPLIER_ID TEXT,
            SUPPLIER_NAME TEXT,
            COUNTRY TEXT,
            CREATED_ON DATE,
            PRIMARY KEY (MANDT, SUPPLIER_ID)
        );
    """,

    "zpo_header": """
        CREATE TABLE IF NOT EXISTS zpo_header (
            MANDT TEXT,
            PO_NUMBER TEXT,
            SUPPLIER_ID TEXT,
            PO_DATE DATE,
            PO_AMOUNT TEXT,
            CURRENCY TEXT,
            PRIMARY KEY (MANDT, PO_NUMBER)
        );
    """,

    "zpo_item": """
        CREATE TABLE IF NOT EXISTS zpo_item (
            MANDT TEXT,
            PO_NUMBER TEXT,
            PO_ITEM TEXT,
            MATERIAL TEXT,
            QUANTITY REAL,
            UNIT TEXT,
            NET_AMOUNT TEXT,
            CURRENCY TEXT,
            PRIMARY KEY (MANDT, PO_NUMBER, PO_ITEM)
        );
    """,

    "zgr_header": """
        CREATE TABLE IF NOT EXISTS zgr_header (
            MANDT TEXT,
            GR_NUMBER TEXT,
            PO_NUMBER TEXT,
            GR_DATE DATE,
            GR_AMOUNT TEXT,
            CURRENCY TEXT,
            PRIMARY KEY (MANDT, GR_NUMBER)
        );
    """,

    "zmatdoc_flight": """
        CREATE TABLE IF NOT EXISTS zmatdoc_flight (
            MANDT TEXT,
            MAT_DOC_NO TEXT,
            GR_NUMBER TEXT,
            PO_NUMBER TEXT,
            SUPPLIER_ID TEXT,
            FLIGHT_NO TEXT,
            FLIGHT_DATE DATE,
            SECTOR TEXT,
            AMOUNT TEXT,
            DESCRIPTION TEXT,
            CURRENCY TEXT,
            PRIMARY KEY (MANDT, MAT_DOC_NO)
        );
    """
}
