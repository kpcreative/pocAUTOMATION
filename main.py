from sap_gui.tables import TABLES
from sap_gui.extract_table import extract_table
import time
from data.clipboard_reader import read_clipboard_table
from data.loaders import save_dataframe
from data.normalize import inject_mandt_if_missing, normalize_dataframe
from sap_gui.connect import get_sap_client,get_sap_session



def run_pipeline():
        # 🔹 1. Create SAP session ONCE
    session = get_sap_session()

    # 🔹 2. Read client (MANDT) ONCE---taki jo SAP me MANDT column hai na usko fill kar sake ye
    client = get_sap_client(session)
    for table in TABLES:
      print("\n" + "=" * 60)
      print(f"Processing table: {table}")

      extract_table(table)

      print("📋 Data is now in clipboard")
     
      
      df=read_clipboard_table()
      df = inject_mandt_if_missing(df, table, client)
      df = normalize_dataframe(df, table)
      print(f"✅ Read {len(df)} rows from clipboard for table {table}")
      
      save_dataframe(df, table)
      
      print(f"💾 Saved data to database for table {table}")
      
if __name__ == "__main__":
    run_pipeline()      
