# src/load_sqlite.py
import sqlite3
import pandas as pd
from datetime import datetime

TABLE = "ads_by_lan_yrkesgrupp"

def ensure_table(conn: sqlite3.Connection):
    conn.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE} (
        date TEXT NOT NULL,
        lan_code TEXT NOT NULL,
        yrkesgrupp TEXT NOT NULL,
        ads_count INTEGER NOT NULL,
        created_at TEXT NOT NULL
    );
    """)
    conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{TABLE}_date ON {TABLE}(date);")

def upsert_for_dates(df: pd.DataFrame, db_path: str = "af_ads.db") -> int:
    if df.empty:
        return 0
    conn = sqlite3.connect(db_path)
    try:
        ensure_table(conn)
        for d in df["date"].unique():
            conn.execute(f"DELETE FROM {TABLE} WHERE date = ?", (d,))
            conn.commit()
            sub = df[df["date"] == d].copy()
            sub["created_at"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
            sub.to_sql(TABLE, conn, if_exists="append", index=False)
        return len(df)
    finally:
        conn.close()
