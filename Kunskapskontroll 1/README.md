# Kunskapskontroll 1 – Arbetsförmedlingen API

# Kunskapskontroll 1 – Arbetsförmedlingen API

Detta projekt är en del av kursen *Python fördjupat* och visar ett automatiserat ETL-flöde:
- **Extract:** hämtar platsannonser från Arbetsförmedlingens API
- **Transform:** normaliserar och aggregerar (datum × län × yrkesgrupp)
- **Load:** skriver till en SQLite-tabell

## Projektstruktur

## Struktur
Kunskapskontroll 1/
├── reports/
│ ├── lan_totals_<datum><tid>.csv
│ ├── report<datum><tid>.xlsx
│ ├── top_by_lan<datum><tid>.csv
│ └── top10_overall<datum>_<tid>.csv
├── src/
│ ├── fetch.py
│ ├── init.py
│ ├── load_sqlite.py
│ └── transform.py
├── tests/
│ ├── test_transform.py
│ └── check_fetch.py
├── .gitignore
├── af_ads.db
├── kunskapskontroll_1.pdf
├── main.py
├── pipeline.log
├── README.md
├── report.py
└── requirements.txt

## Rapport
Skapa CSV/Excel‑rapporter för senaste datum i databasen:
```bash
python report.py


## Installation
1. Klona eller ladda ner projektet.
2. Installera beroenden:
   ```bash
   pip install -r requirements.txt

python main.py

python report.py

## För att få Excel med diagram:

pip install XlsxWriter

Test 
pytest tests/

## Automatisering (Windows Task Scheduler)
Create Basic Task → namn: AF_ETL_Pipeline

Trigger: Daily (t.ex. 07:30)

Action: Start a program

Program/script: sökväg till python.exe

Add arguments: sökväg till main.py

Start in: mappen där main.py ligger