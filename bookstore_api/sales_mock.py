"""Typed sales mock with simple payment simulation and order store.

This remains in-memory for demo purposes but uses clearer types and
immutable returns to make the code easier to reuse.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
from uuid import uuid4
from copy import deepcopy
from threading import Lock


@dataclass
class Order:
    order_id: str
    customer_id: str
    items: List[dict]
    total: float
    payment_tx_id: str
    status: str = 'created'


_orders: Dict[str, Order] = {}
_lock = Lock()


def process_payment(amount: float, payment_info: Optional[dict]) -> tuple[bool, Any]:
    """Simulate a payment gateway call. Returns (success, transaction_id or error)."""
    if not payment_info or not payment_info.get('card_number'):
        return False, 'Missing card details'
    if amount <= 0:
        return False, 'Invalid amount'
    tx_id = str(uuid4())
    return True, tx_id


def create_order(customer_id: str, items: List[dict], total: float, payment_tx_id: str) -> dict:
    order_id = str(uuid4())
    order = Order(order_id=order_id, customer_id=customer_id, items=deepcopy(items), total=total, payment_tx_id=payment_tx_id)
    with _lock:
        _orders[order_id] = order
    return deepcopy(asdict(order))


def get_order(order_id: str) -> Optional[dict]:
    with _lock:
        o = _orders.get(order_id)
        return deepcopy(asdict(o)) if o else None


def list_orders() -> List[dict]:
    with _lock:
        return deepcopy([asdict(o) for o in _orders.values()])
