from logic.inference_logic import *

print(get_po_numbers_for_supplier_service_date(
    "SUPP0001", "jet fuel", "2023-01-05"
))

print(get_gr_numbers_for_supplier_service_date(
    "SUPP0001", "jet fuel", "2023-01-05"
))

print(get_service_delivery_timeline(
    "450000005", "jet fuel"
))
