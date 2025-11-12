# Assignment: Integrating Multiple Data Sources into a Centralized Database

This folder demonstrates a small, runnable integration of two data sources (customer DB and product CSV) into a centralized SQLite database, with schema, sample data, integration script, queries and a short report.

Files
- `create_source_db.py` — generates a sample source SQLite DB (`customers_source.db`) containing the customer data system.
- `products.csv` — sample product data (external CSV).
- `schema.sql` — CREATE TABLE statements for the central database (SQLite compatible).
- `integrate.py` — integration script: reads `customers_source.db` and `products.csv` and loads into `central.db`, creates sample orders and enforces FK relationships.
- `queries.sql` — SQL queries to retrieve combined data and analytics (orders per customer, revenue per product, etc.).
- `er_diagram.puml` — PlantUML ER diagram for the schema.
- `report.md` — short report summarizing the integration process and validation steps.

Requirements
- Python 3.8+ (stdlib `sqlite3`, `csv` used). No external packages required.
- Optional: `pandoc` and PlantUML to render docs and diagrams.

Quick run (PowerShell)

```powershell
cd "c:\Users\jeff\Projects\data_engineering\assignment_integration"
python .\create_source_db.py    # creates customers_source.db
python .\integrate.py          # creates central.db and imports products and customers, creates sample orders
# Inspect central.db (SQLite) with any client, or run queries from queries.sql using sqlite3:
sqlite3 central.db ".read queries.sql"
```

Notes
- The integration script demonstrates validation and simple deduplication. In production you'd use more robust MDM/CDC and transactional guarantees.
