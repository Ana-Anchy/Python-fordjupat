# main.py
import logging
import argparse
from datetime import datetime
from src.transform import get_aggregated
from src.load_sqlite import upsert_for_dates

def setup_logging(level: str = "INFO", log_file: str = "pipeline.log"):
 
    lvl = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=lvl,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ],
    )

def parse_args():
    p = argparse.ArgumentParser(description="AF ETL pipeline")
    p.add_argument("--limit", type=int, default=50, help="broj oglasa po stranici (stable: 50)")
    p.add_argument("--pages", type=int, default=10, help="broj stranica za preuzimanje (npr. 10 => ~500 oglasa)")
    p.add_argument("--log-level", default="INFO", help="DEBUG/INFO/WARNING/ERROR")
    p.add_argument("--db", default="af_ads.db", help="putanja do SQLite baze")
    return p.parse_args()

def main():
    args = parse_args()
    setup_logging(args.log_level)

    logging.info("===== Pipeline start =====")
    logging.info(f"Params: limit={args.limit}, pages={args.pages}, db='{args.db}'")

    try:
        # 1) fetch+transform+aggregate
        agg = get_aggregated(limit=args.limit, pages=args.pages)
        logging.info(f"Aggregated rows: {len(agg)}")

        # 2) load to SQLite
        loaded = upsert_for_dates(agg, db_path=args.db)
        logging.info(f"Loaded rows: {loaded}")

        # 3) done
        print(f"OK. Aggregated rows: {len(agg)}. Loaded: {loaded}")
        logging.info("===== Pipeline success =====")
    except Exception as e:
        logging.exception("Pipeline failed with an error")
        print("Pipeline failed. See pipeline.log for details.")
        raise

if __name__ == "__main__":
    main()

