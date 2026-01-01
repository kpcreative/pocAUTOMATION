import time
from sap_gui.connect import get_sap_session
import os



def extract_table(table_name):
    """
    Extracts all visible rows from SE16N ALV grid
    for the given table name.
    Returns list of dictionaries.
    """

    session = get_sap_session()
    
    # session.findById("wnd[0]/usr/txtRSYST-MANDT").text = "550"
    # session.findById("wnd[0]/usr/txtRSYST-BNAME").text = "I769395"
    # session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = "kartIK098$"
    # session.findById("wnd[0]/usr/pwdRSYST-BCODE").setFocus()
    
    # session.findById("wnd[0]").sendVKey(0)
    # time.sleep(5)
    
    # Go to SE16N
    session.findById("wnd[0]/tbar[0]/okcd").text = "/nSE16N"
    session.findById("wnd[0]").sendVKey(0)
    time.sleep(2)

    # Enter table name
    session.findById("wnd[0]/usr/ctxtGD-TAB").text = table_name
    session.findById("wnd[0]/usr/ctxtGD-TAB").caretPosition = 9
    session.findById("wnd[0]/tbar[1]/btn[8]").press()
    time.sleep(2)

    # Execute
    session.findById("wnd[0]/tbar[1]/btn[8]").press()
    time.sleep(3)

    grid = session.findById("wnd[0]/shellcont/shell")
    grid.pressToolbarContextButton("&MB_EXPORT")
    grid.selectContextMenuItem("&PC")
        
    session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[4,0]").select()
    session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[4,0]").setFocus()

    time.sleep(2)

   
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    print(f"✅ Export triggered for table {table_name}")
    print(f"📁 File saved i clipboard")