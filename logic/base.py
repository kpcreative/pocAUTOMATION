import sqlite3
import pandas as pd
from decimal import Decimal

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "sap_mm_ai.db")


def fetch_df(query, params=None):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df
