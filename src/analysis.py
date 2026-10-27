import pandas as pd
import numpy as np

REQUIRED_COLUMNS = {"session_id","session_date","device","channel","country","landing_page",
                    "page_views","session_seconds","cart_adds","converted","order_value"}

def load_data(path="data/sessions.csv"):
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df["session_date"] = pd.to_datetime(df["session_date"], errors="coerce")
    for col in ["page_views","session_seconds","cart_adds","converted","order_value"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["session_id","session_date","converted"]).drop_duplicates("session_id")
    df["converted"] = df["converted"].astype(int).clip(0,1)
    for col in ["page_views","session_seconds","cart_adds","order_value"]:
        df[col] = df[col].fillna(0).clip(lower=0)
    return df

def overall_kpis(df):
    sessions = len(df)
    conversions = int(df["converted"].sum())
    revenue = float(df["order_value"].sum())
    return {"sessions": sessions, "conversions": conversions,
            "conversion_rate": conversions/sessions*100 if sessions else 0,
            "revenue": revenue, "average_order_value": revenue/conversions if conversions else 0,
            "revenue_per_session": revenue/sessions if sessions else 0}

def grouped_performance(df, dimension):
    if dimension not in df.columns:
        raise ValueError(f"Unknown dimension: {dimension}")
    out = df.groupby(dimension, dropna=False).agg(
        sessions=("session_id","count"), conversions=("converted","sum"),
        revenue=("order_value","sum"), avg_session_seconds=("session_seconds","mean")).reset_index()
    out["conversion_rate"] = np.where(out.sessions > 0, out.conversions/out.sessions*100, 0)
    out["revenue_per_session"] = np.where(out.sessions > 0, out.revenue/out.sessions, 0)
    return out.sort_values("conversion_rate", ascending=False)

def daily_performance(df):
    out = df.groupby(df["session_date"].dt.date).agg(
        sessions=("session_id","count"), conversions=("converted","sum"), revenue=("order_value","sum")
    ).reset_index(names="date")
    out["conversion_rate"] = np.where(out.sessions > 0, out.conversions/out.sessions*100, 0)
    return out
