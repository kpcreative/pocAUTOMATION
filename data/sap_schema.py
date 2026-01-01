SAP_SCHEMA = {
    "ZSUPPLIER": {
        "MANDT": "CLNT",
        "SUPPLIER_ID": "CHAR",
        "SUPPLIER_NAME": "CHAR",
        "COUNTRY": "CHAR",
        "CREATED_ON": "DATS",
    },

    "ZPO_HEADER": {
        "MANDT": "CLNT",
        "PO_NUMBER": "CHAR",
        "SUPPLIER_ID": "CHAR",
        "PO_DATE": "DATS",
        "PO_AMOUNT": "CURR",
        "CURRENCY": "CUKY",
    },

    "ZPO_ITEM": {
        "MANDT": "CLNT",
        "PO_NUMBER": "CHAR",
        "PO_ITEM": "NUMC",
        "MATERIAL": "CHAR",
        "QUANTITY": "QUAN",
        "UNIT": "UNIT",
        "NET_AMOUNT": "CURR",
        "CURRENCY": "CUKY",
    },

    "ZGR_HEADER": {
        "MANDT": "CLNT",
        "GR_NUMBER": "CHAR",
        "PO_NUMBER": "CHAR",
        "GR_DATE": "DATS",
        "GR_AMOUNT": "CURR",
        "CURRENCY": "CUKY",
    },

    "ZMATDOC_FLIGHT": {
        "MANDT": "CLNT",
        "MAT_DOC_NO": "CHAR",
        "GR_NUMBER": "CHAR",
        "PO_NUMBER": "CHAR",
        "SUPPLIER_ID": "CHAR",
        "FLIGHT_NO": "CHAR",
        "FLIGHT_DATE": "DATS",
        "SECTOR": "CHAR",
        "AMOUNT": "CURR",
        "DESCRIPTION": "CHAR",
        "CURRENCY": "CUKY",
    },
}
