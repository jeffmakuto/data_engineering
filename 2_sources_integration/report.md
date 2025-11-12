# Integration Report

Project: Integrating Multiple Data Sources into a Centralized Database

Summary
This demo integrates customer data from a simulated relational source (`customers_source.db`) and product data from an external CSV (`products.csv`) into a centralized SQLite database (`central.db`). The integration demonstrates schema design, data validation, deduplication, referential integrity, and example queries for insights.

Process
1. Source generation
- `create_source_db.py` creates `customers_source.db` with sample customer records (including a near-duplicate to show deduplication). 

2. Schema
- The central schema (`schema.sql`) contains `customers`, `products`, `orders`, and `order_items`. Foreign keys enforce relationships.

3. Integration
- `integrate.py` reads customers from the source DB and products from the CSV, applies basic validation, and upserts into `central.db`.
- Deduplication logic attempts to match existing customers by email or phone; if found, records are merged.
- The script also creates sample orders linking customers to products and computes line totals and order totals.

4. Validation and data quality
- The integration script prints skipped rows (missing required fields) and parse errors.
- Referential integrity relies on foreign keys in SQLite; missing product IDs are skipped for order lines.

5. Queries and reports
- `queries.sql` contains queries to: list orders with product details, total spent per customer, filter products by price range, identify high-value customers, and report product revenue.

Limitations and next steps
- This is a small demo using SQLite and CSVs. Production systems should use transactional CDC, MDM, and stronger data quality tooling.
- Future improvements: implement probabilistic matching, audit logs, incremental ingestion, and a data warehouse for analytics.

How to run
See the README in this folder. The whole demo runs with Python and produces `central.db` that can be inspected with `sqlite3` or any DB client.
