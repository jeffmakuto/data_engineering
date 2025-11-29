# Bookstore API — Design & Implementation

## Executive summary
This repository contains a lightweight, production-minded demonstration API for a bookstore. It integrates three clear, typed subsystems (Inventory, Sales, Delivery) and exposes a small set of HTTP endpoints for listing books, placing orders, and scheduling deliveries.

Key design goals:
- Practical, testable code that resembles production patterns.
- Clear API contract (OpenAPI) and interactive docs.
- Minimal external dependencies and reproducible development experience.


## Architecture and design (modernized)
- Framework: FastAPI — type-first, async-ready, and auto-generates OpenAPI/Swagger UI.
- Subsystems: modular in-memory services implemented with dataclasses and typed APIs:
  - `inventory_mock.py` — typed Book dataclass, thread-safe in-memory store.
  - `sales_mock.py` — typed Order dataclass, simple payment simulation, thread-safe store.
  - `delivery_mock.py` — typed Delivery dataclass and scheduling.
- Endpoints (same semantics as before):
  - `GET /api/books/{isbn}` — fetch book details.
  - `GET /api/books` — list inventory.
  - `POST /api/orders` — place an order (validates items, processes payment, reserves stock, creates order).
  - `GET /api/orders/{order_id}` — fetch order details.
  - `POST /api/delivery` — schedule a delivery for an order.
- Authentication: API key via the `X-API-Key` header (demo secret `secret123`). For production, switch to OAuth2/JWT and secrets management.


## Implementation notes (developer-focused)
- Input validation is handled by Pydantic models; the server surface is strongly typed which improves both dev UX and runtime safety.
- Inventory reservation and order creation are done atomically within the in-memory store (protected by locks) for the demo. In production, move this to a durable database and consider optimistic locking or transactional patterns.
- The payment flow is intentionally simplified — `sales_mock.process_payment` simulates approval and returns a UUID transaction id. Swap with a real gateway for production.


## Testing
- Tests are in `tests/test_api.py` and use FastAPI's `TestClient` (Starlette) for end-to-end-style unit tests.
- The test suite covers:
  - Authentication enforcement.
  - Book retrieval and not-found behavior.
  - Order placement with payment and inventory reservation.
  - Delivery scheduling for created orders.


## Security and limitations
- The project is a demo: do not use the in-memory stores for production workloads.
- No PCI compliance or real payment handling is implemented — treat `sales_mock` as a placeholder.


## How to run (developer)
1. Create and activate a Python virtual environment.

   PowerShell:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

2. Start the API locally:

   ```powershell
   uvicorn app:app --reload --port 5001
   ```

3. Open interactive docs at `http://127.0.0.1:5001/docs`.


## Next steps and production-readiness
- Persist state to a relational database with migrations (Alembic) and add integration tests.
- Introduce idempotency keys and durable message queues for asynchronous processing.
- Add structured logging, metrics (Prometheus), and health endpoints.
- Containerize the app (Dockerfile) for reproducible CI/CD and local runs.


