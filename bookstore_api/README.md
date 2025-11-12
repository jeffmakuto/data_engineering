# Bookstore API Demo

This folder contains a small Flask-based REST API that integrates three mocked subsystems: Inventory, Sales, and Delivery.

Quick start

1. Create a virtualenv and install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the API

```powershell
set BOOKSTORE_API_KEY=secret123
python app.py
```

3. Open Swagger UI

Navigate to http://localhost:5001/docs to see interactive API docs.

Testing

```powershell
pytest -q
```

Notes
- The service uses a very simple API key auth via header `X-API-Key`.
- The subsystems are mocked with in-memory modules (`inventory_mock`, `sales_mock`, `delivery_mock`).
- This is a demo. For production, use persistent storage, proper payment gateway integration, and secure secret management.
