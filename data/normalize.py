from data.sap_schema import SAP_SCHEMA
from data import sap_type_converters as conv
from data.sap_schema import SAP_SCHEMA

TYPE_MAP = {
    "CLNT": conv.clnt,
    "CHAR": conv.char,
    "NUMC": conv.numc,
    "DATS": conv.dats,
    "CURR": conv.curr,
    "QUAN": conv.quan,
    "CUKY": conv.cuky,
    "UNIT": conv.unit,
}

def inject_mandt_if_missing(df, table_name, mandt):
    table_name = table_name.upper()
    schema = SAP_SCHEMA.get(table_name, {})

    # If MANDT is part of SAP schema but missing in data
    if "MANDT" in schema and "MANDT" not in df.columns:
        df.insert(0, "MANDT", str(mandt))

    return df

def normalize_dataframe(df, table_name):
    table_name = table_name.upper()

    if table_name not in SAP_SCHEMA:
        raise ValueError(f"No SAP schema defined for table {table_name}")

    schema = SAP_SCHEMA[table_name]

    for column, sap_type in schema.items():
        if column not in df.columns:
               raise ValueError(
                 f"Column {column} missing in extracted data for table {table_name} "
                 f"(not injected)"
                )


        if sap_type not in TYPE_MAP:
            raise ValueError(
                f"No converter defined for SAP type {sap_type}"
            )

        df[column] = TYPE_MAP[sap_type](df[column])

    return df
