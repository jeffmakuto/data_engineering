"""
Simple Delivery mock service: stores delivery tasks in-memory.
"""
from uuid import uuid4
from copy import deepcopy

_deliveries = {}


def create_delivery(order_id, address, courier=None):
    delivery_id = str(uuid4())
    d = {
        'delivery_id': delivery_id,
        'order_id': order_id,
        'address': address,
        'courier': courier or 'local',
        'status': 'scheduled'
    }
    _deliveries[delivery_id] = d
    return deepcopy(d)


def update_delivery_status(delivery_id, status):
    d = _deliveries.get(delivery_id)
    if not d:
        return None
    d['status'] = status
    return deepcopy(d)


def get_delivery(delivery_id):
    d = _deliveries.get(delivery_id)
    return deepcopy(d) if d else None


def list_deliveries():
    return deepcopy(list(_deliveries.values()))
