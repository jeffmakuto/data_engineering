import os
import json
import pytest

from fastapi.testclient import TestClient
from app import app

API_KEY = 'secret123'


@pytest.fixture
def client():
    client = TestClient(app)
    yield client

def test_get_book_success(client):
    r = client.get('/api/books/9780143127550', headers={'X-API-Key': API_KEY})
    assert r.status_code == 200
    data = r.json()
    assert data['isbn'] == '9780143127550'

def test_get_book_not_found(client):
    r = client.get('/api/books/0000000000', headers={'X-API-Key': API_KEY})
    assert r.status_code == 404

def test_place_order_and_delivery_flow(client):
    # place an order
    payload = {
        'customer_id': 'cust-1',
        'items': [{'isbn': '9780143127550', 'quantity': 1}],
        'payment': {'card_number': '4111111111111111', 'expiry': '12/26'}
    }
    r = client.post('/api/orders/', json=payload, headers={'X-API-Key': API_KEY})
    assert r.status_code == 201
    body = r.json()
    assert 'order_id' in body
    order_id = body['order_id']

    # create delivery
    d_payload = {'order_id': order_id, 'address': '123 Main St'}
    rd = client.post('/api/delivery/', json=d_payload, headers={'X-API-Key': API_KEY})
    assert rd.status_code == 201
    delivery = rd.json()
    assert delivery['order_id'] == order_id

def test_auth_required(client):
    r = client.get('/api/books/9780143127550')
    assert r.status_code == 401
