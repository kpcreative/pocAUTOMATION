from data.db import get_connection
from data.schema_sql import SCHEMA_SQL
from decimal import Decimal

def ensure_table_exists(table_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(SCHEMA_SQL[table_name])
    conn.commit()
    conn.close()


def save_dataframe(df, table_name):
    table_name = table_name.lower()

    # ensure table exists
    ensure_table_exists(table_name)

    # convert Decimal → string for SQLite
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: str(x) if isinstance(x, Decimal) else x
        )

    conn = get_connection()
    cursor = conn.cursor()

    columns = df.columns.tolist()
    placeholders = ",".join(["?"] * len(columns))
    col_names = ",".join(columns)

    sql = f"""
        INSERT OR IGNORE INTO {table_name}
        ({col_names})
        VALUES ({placeholders})
    """

    cursor.executemany(sql, df.values.tolist())
    conn.commit()
    conn.close()
