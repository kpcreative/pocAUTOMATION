import pyperclip
import pandas as pd

def read_clipboard_table():
    text = pyperclip.paste()

    if not text or "|" not in text:
        raise ValueError("Clipboard does not contain SAP table data")

    lines = text.splitlines()

    cleaned_lines = []
    for line in lines:
        line = line.strip()

        # skip empty lines
        if not line:
            continue

        # skip separator lines like ------
        if set(line) == {"-"}:
            continue

        # keep only table rows
        if line.startswith("|") and line.endswith("|"):
            cleaned_lines.append(line)

    if not cleaned_lines:
        raise ValueError("No valid table rows found in clipboard")

    # header
    header_line = cleaned_lines[0]
    headers = [h.strip().upper() for h in header_line.split("|")[1:-1]]

    data_rows = []
    for line in cleaned_lines[1:]:
        values = [v.strip() for v in line.split("|")[1:-1]]
        if len(values) == len(headers):
            data_rows.append(values)

    df = pd.DataFrame(data_rows, columns=headers)
    return df
