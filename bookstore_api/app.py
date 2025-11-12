"""
Bookstore Management API (Flask + flask-restx)
Endpoints:
- GET /api/books/<isbn>
- POST /api/orders
- POST /api/delivery
Simple API key auth: header 'X-API-Key'.
Uses the inventory_mock, sales_mock, and delivery_mock modules.
Swagger UI available at /docs
"""
import os
from functools import wraps
from decimal import Decimal
from flask import Flask, request, jsonify
import werkzeug
try:
    # Python 3.8+ provides importlib.metadata
    from importlib import metadata as importlib_metadata
except Exception:
    import importlib_metadata

# Some newer werkzeug releases removed the __version__ attribute which
# older Flask testing utilities expect. Provide a compatibility shim so
# the test client can construct a default User-Agent string.
try:
    if not hasattr(werkzeug, '__version__'):
        try:
            werkzeug.__version__ = importlib_metadata.version('werkzeug')
        except Exception:
            werkzeug.__version__ = '0'
except Exception:
    # Best effort; do not fail import if metadata isn't available
    pass

from inventory_mock import get_book, reserve_stock, list_inventory
from sales_mock import process_payment, create_order, get_order
from delivery_mock import create_delivery

API_KEY = os.environ.get('BOOKSTORE_API_KEY', 'secret123')


def create_app():
    app = Flask(__name__)

    def require_api_key(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = request.headers.get('X-API-Key')
            if not key or key != API_KEY:
                return jsonify({'message': 'Unauthorized'}), 401
            return f(*args, **kwargs)
        return wrapper

    @app.route('/api/books/', methods=['GET'])
    @require_api_key
    def list_books():
        return jsonify(list_inventory())

    @app.route('/api/books/<string:isbn>', methods=['GET'])
    @require_api_key
    def get_book_route(isbn):
        book = get_book(isbn)
        if not book:
            return jsonify({'message': 'Book not found'}), 404
        return jsonify(book)

    @app.route('/api/orders/', methods=['POST'])
    @require_api_key
    def create_order_route():
        data = request.get_json(silent=True) or {}
        customer_id = data.get('customer_id')
        items = data.get('items', [])
        payment = data.get('payment')

        # Validate items and compute total
        total = Decimal('0.0')
        for it in items:
            isbn = it.get('isbn')
            qty = int(it.get('quantity', 0))
            if qty <= 0:
                return jsonify({'message': 'Quantity must be positive'}), 400
            book = get_book(isbn)
            if not book:
                return jsonify({'message': f'Book {isbn} not found'}), 400
            total += Decimal(str(book['price'])) * qty

        # Process payment
        ok, result = process_payment(float(total), payment)
        if not ok:
            return jsonify({'message': f'Payment failed: {result}'}), 402
        tx_id = result

        # Reserve stock
        for it in items:
            isbn = it['isbn']
            qty = int(it['quantity'])
            success, msg = reserve_stock(isbn, qty)
            if not success:
                return jsonify({'message': f'Inventory issue for {isbn}: {msg}'}), 409

        # Create order record in sales mock
        order = create_order(customer_id, items, float(total), tx_id)
        return jsonify({'order_id': order['order_id'], 'status': order['status'], 'total': order['total']}), 201

    @app.route('/api/orders/<string:order_id>', methods=['GET'])
    @require_api_key
    def get_order_route(order_id):
        order = get_order(order_id)
        if not order:
            return jsonify({'message': 'Order not found'}), 404
        return jsonify(order)

    @app.route('/api/delivery/', methods=['POST'])
    @require_api_key
    def create_delivery_route():
        data = request.get_json(silent=True) or {}
        order_id = data.get('order_id')
        address = data.get('address')
        courier = data.get('courier')
        if not order_id or not address:
            return jsonify({'message': 'order_id and address required'}), 400
        d = create_delivery(order_id, address, courier)
        return jsonify(d), 201

    # Serve OpenAPI spec
    @app.route('/openapi.yaml', methods=['GET'])
    def serve_openapi():
        from flask import send_from_directory
        return send_from_directory('.', 'openapi.yaml')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)
