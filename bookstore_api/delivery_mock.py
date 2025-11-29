"""Delivery mock: typed, thread-safe in-memory delivery tasks."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from uuid import uuid4
from copy import deepcopy
from threading import Lock


@dataclass
class Delivery:
    delivery_id: str
    order_id: str
    address: str
    courier: str
    status: str = 'scheduled'


_deliveries: Dict[str, Delivery] = {}
_lock = Lock()


def create_delivery(order_id: str, address: str, courier: Optional[str] = None) -> dict:
    delivery_id = str(uuid4())
    d = Delivery(delivery_id=delivery_id, order_id=order_id, address=address, courier=courier or 'local')
    with _lock:
        _deliveries[delivery_id] = d
    return deepcopy(asdict(d))


def update_delivery_status(delivery_id: str, status: str) -> Optional[dict]:
    with _lock:
        d = _deliveries.get(delivery_id)
        if not d:
            return None
        d.status = status
        return deepcopy(asdict(d))


def get_delivery(delivery_id: str) -> Optional[dict]:
    with _lock:
        d = _deliveries.get(delivery_id)
        return deepcopy(asdict(d)) if d else None


def list_deliveries() -> List[dict]:
    with _lock:
        return deepcopy([asdict(d) for d in _deliveries.values()])
