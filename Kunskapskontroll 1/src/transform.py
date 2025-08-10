# src/transform.py
import pandas as pd
from typing import List, Dict, Any
from .fetch import fetch

def normalize(hits: List[Dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for ad in hits:
        pub = ad.get("publication_date") or ""
        date = pub[:10] if isinstance(pub, str) else None

        wla = ad.get("workplace_address") or {}
        lan = wla.get("region_code")
        if not lan:
            muni = wla.get("municipality_code")
            if muni:
                lan = str(muni)[:2]

        og = ad.get("occupation_group") or {}
        occ_label = og.get("label") or (ad.get("occupation") or {}).get("label")

        if date and lan and occ_label:
            rows.append({"date": date, "lan_code": str(lan), "yrkesgrupp": occ_label})
    return pd.DataFrame(rows)

def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    return (df.groupby(["date", "lan_code", "yrkesgrupp"])
              .size()
              .reset_index(name="ads_count"))

def get_aggregated(limit: int = 50, pages: int = 10) -> pd.DataFrame:
    hits = fetch(limit=limit, max_pages=pages, debug=True)
    print(f"[debug] raw hits: {len(hits)}")
    df = normalize(hits)
    print(f"[debug] rows after normalize (date+lan+yrkesgrupp present): {len(df)}")
    return aggregate(df)



