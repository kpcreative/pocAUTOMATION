# sap_gui/connect.py

import win32com.client
import sys
import time

def get_sap_client(session):
    """
    Returns SAP client (MANDT) from current session
    """
    return session.Info.Client

def get_sap_session():
    """
    Connects to an already open SAP GUI session
    and returns the session object.
    """

    try:
        # Get SAP GUI object
        sap_gui_auto = win32com.client.GetObject("SAPGUI")
    except Exception:
        print("❌ SAP GUI is not running.")
        sys.exit(1)

    try:
        application = sap_gui_auto.GetScriptingEngine
        connection = application.Children(0)
        session = connection.Children(0)
    except Exception:
        print("❌ Could not connect to SAP session.")
        sys.exit(1)

    print("✅ Connected to SAP GUI session")
    return session
