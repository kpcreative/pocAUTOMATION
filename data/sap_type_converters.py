import pandas as pd
from decimal import Decimal

def clnt(series):
    return series.astype(str)

def char(series):
    return series.astype(str)

def numc(series):
    return series.astype(str)

def dats(series):
    return pd.to_datetime(
        series, format="%d.%m.%Y", errors="coerce"
    ).dt.date

def curr(series):
    return series.apply(
        lambda x: Decimal(
            x.replace(".", "").replace(",", ".")
        ) if pd.notna(x) else None
    )

def quan(series):
    return pd.to_numeric(series, errors="coerce")

def cuky(series):
    return series.astype(str)

def unit(series):
    return series.astype(str)
