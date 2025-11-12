# Bookstore API — Design & Implementation Report

## Overview
This project implements a small RESTful API that integrates three mock subsystems common to a bookstore: Inventory, Sales, and Delivery. The service is intended as a demonstration of integration patterns, simple authentication, API documentation (Swagger), and basic tests.

## Architecture and Design
- Framework: Flask with `flask-restx` to provide REST endpoints and automatic Swagger UI.
- Subsystems: implemented as separate in-memory modules:
  - `inventory_mock.py` — manages book data and stock levels.
  - `sales_mock.py` — simulates payment processing and order persistence.
  - `delivery_mock.py` — creates delivery tasks and updates status.
- API endpoints:
  - `GET /api/books/{isbn}` — fetch book details.
  - `GET /api/books` — list inventory.
  - `POST /api/orders` — place an order (validates items, processes payment, reserves stock, creates order).
  - `GET /api/orders/{order_id}` — fetch order details.
  - `POST /api/delivery` — schedule a delivery for an order.
- Authentication: API key required via `X-API-Key` header. For demo purposes the default key is `secret123`.
- Data exchange: JSON request/response.
- Documentation: `openapi.yaml` (OpenAPI 3.0 spec) and Swagger UI served at `/docs` when running the app.

## Implementation Notes
- Inventory reservation is performed after payment succeeds; in a production system you'd likely reserve first and use two-phase commit or compensation transactions.
- The sales mock returns a UUID transaction id when payment is simulated as successful.
- The order payload expects `customer_id`, a list of `{ isbn, quantity }`, and a `payment` object that contains minimal card fields for simulation.

## Testing
- Unit tests are located in `tests/test_api.py` and use Flask's test client to exercise endpoints.
- Because local pytest environments can have plugin conflicts, the `run_tests.ps1` helper ensures plugins are not auto-loaded during test execution.
- Test highlights:
  - GET book success and not-found cases.
  - End-to-end order placement flow including payment and inventory reservation.
  - Delivery scheduling follow-up for created orders.

## Security and Limitations
- The demo uses an API key for simplicity. For production use OAuth2/JWT and proper secrets management.
- Payment processing is mocked. Replace `sales_mock.process_payment` with a PCI-compliant gateway integration for real payments.
- State is in-memory: orders, inventory changes, and delivery tasks are not persisted beyond process lifetime.

## How to run
1. Create a virtual environment and install dependencies from `requirements.txt`.
2. Start the API: `python app.py` (ensure `BOOKSTORE_API_KEY` is set to match client requests).
3. Use Swagger UI at `http://localhost:5001/docs` or curl/Postman to exercise endpoints.

## Next steps and improvements
- Persist data to a database (Postgres/SQLite) and add migrations.
- Implement idempotency keys for order creation to handle retries safely.
- Add asynchronous background tasks for delivery processing and payment webhooks.
- Harden authentication and add role-based access control.

