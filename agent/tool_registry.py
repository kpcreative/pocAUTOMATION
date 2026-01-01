# agent/tool_registry.py

from logic.po_logic import *
from logic.gr_logic import *
from logic.match_logic import *
from logic.material_logic import *
from logic.reconciliation_logic import *
from logic.service_value_logic import *
from logic.inference_logic import *
from logic.open_items_logic import *
from logic.exception_logic import *
from logic.data_quality_logic import *
from logic.timeline_logic import *
from logic.supplier_logic import *
from logic.supplier_performance_logic import *

TOOLS = {
    "get_po_by_number": {
        "function": get_po_by_number,
        "required": ["po_number"]
    },
    
    "get_supplier_by_po": {
    "function": get_supplier_by_po,
    "required": ["po_number"]
   }
,
    "get_pos_by_supplier": {
        "function": get_pos_by_supplier,
        "required": ["supplier_id"]
    },
    "po_gr_reconciliation": {
        "function": po_gr_reconciliation,
        "required": ["po_number"]
    },
    "full_po_reconciliation": {
        "function": full_po_reconciliation,
        "required": ["po_number"]
    },
    "reconcile_po_by_service": {
        "function": reconcile_po_by_service,
        "required": ["po_number", "service_text"]
    },
    "reconcile_service_amount": {
        "function": reconcile_service_amount,
        "required": ["po_number", "service_text"]
    },
    "get_po_numbers_for_supplier_service_date": {
        "function": get_po_numbers_for_supplier_service_date,
        "required": ["supplier_id", "service_text", "service_date"]
    },
    "get_gr_numbers_for_supplier_service_date": {
        "function": get_gr_numbers_for_supplier_service_date,
        "required": ["supplier_id", "service_text", "service_date"]
    },
    "get_gr_for_po_service_date": {
        "function": get_gr_for_po_service_date,
        "required": ["po_number", "service_text", "service_date"]
    },
    "get_service_delivery_timeline": {
        "function": get_service_delivery_timeline,
        "required": ["po_number", "service_text"]
    },
    "get_open_services_for_po": {
        "function": get_open_services_for_po,
        "required": ["po_number"]
    },
    "find_service_exceptions": {
        "function": find_service_exceptions,
        "required": ["po_number"]
    },
    "find_orphan_grs": {
        "function": find_orphan_grs,
        "required": []
    },
    "get_delivery_summary": {
        "function": get_delivery_summary,
        "required": ["po_number"]
    },
    "supplier_delivery_snapshot": {
        "function": supplier_delivery_snapshot,
        "required": ["supplier_id"]
    }
}
