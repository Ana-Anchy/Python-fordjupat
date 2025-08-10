# tests/test_transform.py
from src.transform import normalize, aggregate

def test_normalize_and_aggregate():
    sample = [
        {
            "publication_date": "2025-08-10T12:00:00Z",
            "workplace_address": {"region_code": "01"},
            "occupation": {"label": "Dataanalytiker"}
        },
        {
            "publication_date": "2025-08-10T08:00:00Z",
            "workplace_address": {"region_code": "01"},
            "occupation": {"label": "Dataanalytiker"}
        }
    ]
    df = normalize(sample)
    agg = aggregate(df)
    assert len(agg) == 1
    row = agg.iloc[0].to_dict()
    assert row["date"] == "2025-08-10"
    assert row["lan_code"] == "01"
    assert row["yrkesgrupp"] == "Dataanalytiker"
    assert row["ads_count"] == 2
