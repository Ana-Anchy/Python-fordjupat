# src/fetch.py
# src/fetch.py
import time
import requests

BASE = "https://jobsearch.api.jobtechdev.se/search"

def fetch(limit: int = 50, max_pages: int = 10, sleep: float = 0.2, debug: bool = False):
   
    all_hits = []
    offset = 0

    for page in range(max_pages):
        params = {
            "offset": offset,
            "limit": limit,
            # requests će ovo pretvoriti u &include=occupation&include=workplace_address
            "include": ["occupation", "workplace_address"],
        }
        r = requests.get(BASE, params=params, timeout=30)
        if debug:
            print(f"[fetch] {r.url} -> {r.status_code}")
        r.raise_for_status()
        hits = r.json().get("hits", [])

        if not hits:
            if debug:
                print("[fetch] no hits on this page; stopping.")
            break

        all_hits.extend(hits)
        offset += limit
        time.sleep(sleep)

    if debug:
        print(f"[fetch] total hits: {len(all_hits)}")
    return all_hits

