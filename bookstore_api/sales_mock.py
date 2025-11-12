"""
Simple Sales mock service: processes payments and creates orders in-memory.
"""
from uuid import uuid4
from copy import deepcopy

_orders = {}


def process_payment(amount, payment_info):
    """Simulate a payment gateway call. Returns (success, transaction_id or error)."""
    # Very simple simulation: accept if card_number present and amount > 0
    if not payment_info or not payment_info.get('card_number'):
        return False, 'Missing card details'
    if amount <= 0:
        return False, 'Invalid amount'
    # simulate approval
    tx_id = str(uuid4())
    return True, tx_id


def create_order(customer_id, items, total, payment_tx_id):
    order_id = str(uuid4())
    order = {
        'order_id': order_id,
        'customer_id': customer_id,
        'items': deepcopy(items),
        'total': total,
        'payment_tx_id': payment_tx_id,
        'status': 'created'
    }
    _orders[order_id] = order
    return deepcopy(order)


def get_order(order_id):
    order = _orders.get(order_id)
    return deepcopy(order) if order else None


def list_orders():
    return deepcopy(list(_orders.values()))
