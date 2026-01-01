import sqlite3
def get_connection():
    conn = sqlite3.connect("sap_mm_ai.db")
    return conn