
# report.py
import os
import sqlite3
from datetime import datetime, timezone
import pandas as pd

DB = "af_ads.db"
TABLE = "ads_by_lan_yrkesgrupp"
OUT_DIR = "reports"


def ensure_outdir(path=OUT_DIR):
    os.makedirs(path, exist_ok=True)


def load_last_day_df(con) -> tuple[str, pd.DataFrame]:
    last = pd.read_sql_query(f"SELECT MAX(date) AS d FROM {TABLE}", con)["d"].iloc[0]
    if not last:
        raise RuntimeError("No data found in table.")
    df = pd.read_sql_query(
        f"""
        SELECT date, lan_code, yrkesgrupp, ads_count
        FROM {TABLE}
        WHERE date = ?
        """,
        con,
        params=(last,),
    )
    return last, df


def make_reports():
    ensure_outdir()
    con = sqlite3.connect(DB)

    try:
        last_date, df = load_last_day_df(con)

        # Top 10 overall (yrkesgrupp)
        top10 = (
            df.groupby("yrkesgrupp", as_index=False)["ads_count"]
              .sum().sort_values("ads_count", ascending=False)
              .head(10)
        )

        # Pivot: yrkesgrupp x län
        by_lan = df.pivot_table(
            index="yrkesgrupp",
            columns="lan_code",
            values="ads_count",
            aggfunc="sum",
            fill_value=0,
        )

        # Suma po län
        lan_totals = (
            df.groupby("lan_code", as_index=False)["ads_count"]
              .sum().sort_values("ads_count", ascending=False)
        )

        # Snimanje CSV fajlova
        stamp = f"{last_date}_{datetime.now(timezone.utc).strftime('%H%M%S')}"
        top10_path = os.path.join(OUT_DIR, f"top10_overall_{stamp}.csv")
        by_lan_path = os.path.join(OUT_DIR, f"top_by_lan_{stamp}.csv")
        lan_totals_path = os.path.join(OUT_DIR, f"lan_totals_{stamp}.csv")

        top10.to_csv(top10_path, index=False, encoding="utf-8")
        by_lan.to_csv(by_lan_path, encoding="utf-8")
        lan_totals.to_csv(lan_totals_path, index=False, encoding="utf-8")

        # Pokušaj Excel sa XlsxWriter (grafik), pa openpyxl (bez grafikona), inače preskoči
        xlsx_path = os.path.join(OUT_DIR, f"report_{stamp}.xlsx")
        excel_saved = False
        chart_added = False

        # probaj engines redom
        for engine in ("xlsxwriter", "openpyxl"):
            try:
                with pd.ExcelWriter(xlsx_path, engine=engine) as xw:
                    # Sheetovi
                    df.to_excel(xw, index=False, sheet_name="raw_last_day")
                    top10.to_excel(xw, index=False, sheet_name="top10_overall")
                    by_lan.to_excel(xw, sheet_name="by_lan")
                    lan_totals.to_excel(xw, index=False, sheet_name="lan_totals")

                    # Ako je XlsxWriter, dodaj bar chart za Top10
                    if engine == "xlsxwriter":
                        wb = xw.book
                        ws = xw.sheets["top10_overall"]

                        # Bar chart – serija je kolona ads_count, kategorije su yrkesgrupp
                        chart = wb.add_chart({"type": "bar"})
                        # rows: od 1 do len(top10), kolone: 0 (yrkesgrupp) i 1 (ads_count)
                        chart.add_series({
                            "name": "Antal annonser",
                            "categories": ["top10_overall", 1, 0, len(top10), 0],
                            "values":     ["top10_overall", 1, 1, len(top10), 1],
                        })
                        chart.set_title({"name": "Top 10 yrkesgrupper"})
                        chart.set_x_axis({"name": "Antal annonser"})
                        chart.set_y_axis({"name": "Yrkesgrupp"})
                        chart.set_style(10)

                        # Ubaci chart na sheet (pored tabele)
                        ws.insert_chart("D2", chart)
                        chart_added = True

                excel_saved = True
                break
            except Exception:
                continue

        # Ispis u konzoli
        print(f"Report date: {last_date}")
        print("\nTop 10 yrkesgrupper (overall):")
        print(top10.to_string(index=False))
        print("\nTotals per län:")
        print(lan_totals.to_string(index=False))

        # Sačuvano
        print("\nSaved:")
        print(" ", top10_path)
        print(" ", by_lan_path)
        print(" ", lan_totals_path)
        if excel_saved:
            print(" ", xlsx_path, "(chart added)" if chart_added else "(no chart)")
        else:
            print(" (Excel skipped: install 'XlsxWriter' or 'openpyxl' to enable .xlsx export)")

    finally:
        con.close()


if __name__ == "__main__":
    make_reports()
