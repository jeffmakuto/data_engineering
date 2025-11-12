"""Modern FastAPI implementation for the Bookstore demo.

This file replaces the previous Flask implementation with a lightweight,
types-first FastAPI app using Pydantic models and dependency-based auth.
"""
from decimal import Decimal
from typing import List, Optional
import os

from fastapi import FastAPI, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field

from inventory_mock import get_book, reserve_stock, list_inventory
from sales_mock import process_payment, create_order, get_order
from delivery_mock import create_delivery

API_KEY = os.environ.get('BOOKSTORE_API_KEY', 'secret123')

app = FastAPI(title='Bookstore API', version='1.0')


def require_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')


class Book(BaseModel):
    isbn: str
    title: Optional[str]
    author: Optional[str]
    price: Optional[float]
    stock: Optional[int]


class OrderItem(BaseModel):
    isbn: str
    quantity: int = Field(..., gt=0)


class OrderRequest(BaseModel):
    customer_id: str
    items: List[OrderItem]
    payment: dict


class OrderResponse(BaseModel):
    order_id: str
    status: str
    total: float


class DeliveryRequest(BaseModel):
    order_id: str
    address: str
    courier: Optional[str]


@app.get('/api/books/', response_model=List[Book], dependencies=[Depends(require_api_key)])
def api_list_books():
    return list_inventory()


@app.get('/api/books/{isbn}', response_model=Book, dependencies=[Depends(require_api_key)])
def api_get_book(isbn: str):
    book = get_book(isbn)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
    return book


@app.post('/api/orders/', response_model=OrderResponse, status_code=201, dependencies=[Depends(require_api_key)])
def api_create_order(req: OrderRequest):
    total = Decimal('0.0')
    for it in req.items:
        book = get_book(it.isbn)
        if not book:
            raise HTTPException(status_code=400, detail=f'Book {it.isbn} not found')
        total += Decimal(str(book['price'])) * it.quantity

    ok, result = process_payment(float(total), req.payment)
    if not ok:
        raise HTTPException(status_code=402, detail=f'Payment failed: {result}')

    tx_id = result
    for it in req.items:
        success, msg = reserve_stock(it.isbn, it.quantity)
        if not success:
            raise HTTPException(status_code=409, detail=f'Inventory issue for {it.isbn}: {msg}')

    order = create_order(req.customer_id, [it.dict() for it in req.items], float(total), tx_id)
    return OrderResponse(order_id=order['order_id'], status=order['status'], total=order['total'])


@app.get('/api/orders/{order_id}', dependencies=[Depends(require_api_key)])
def api_get_order(order_id: str):
    o = get_order(order_id)
    if not o:
        raise HTTPException(status_code=404, detail='Order not found')
    return o


@app.post('/api/delivery/', status_code=201, dependencies=[Depends(require_api_key)])
def api_create_delivery(req: DeliveryRequest):
    if not req.order_id or not req.address:
        raise HTTPException(status_code=400, detail='order_id and address required')
    d = create_delivery(req.order_id, req.address, req.courier)
    return d


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app:app', host='0.0.0.0', port=5001, reload=True)
