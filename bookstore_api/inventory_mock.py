"""
Simple in-memory Inventory mock service.
Provides functions to get book details and reserve stock.
"""
from copy import deepcopy

# Sample inventory keyed by ISBN
_inventory = {
    '9780143127550': {
        'isbn': '9780143127550',
        'title': 'The Martian',
        'author': 'Andy Weir',
        'price': 12.99,
        'stock': 10
    },
    '9780262033848': {
        'isbn': '9780262033848',
        'title': 'Introduction to Algorithms',
        'author': 'Cormen et al.',
        'price': 89.99,
        'stock': 3
    },
    '9780140449136': {
        'isbn': '9780140449136',
        'title': 'The Odyssey',
        'author': 'Homer',
        'price': 9.5,
        'stock': 25
    }
}


def get_book(isbn):
    book = _inventory.get(isbn)
    return deepcopy(book) if book else None


def reserve_stock(isbn, qty):
    """Attempt to reserve qty units of isbn. Returns True if successful, False otherwise."""
    book = _inventory.get(isbn)
    if not book:
        return False, 'Book not found'
    if book['stock'] < qty:
        return False, 'Insufficient stock'
    book['stock'] -= qty
    return True, None


def replenish_stock(isbn, qty):
    book = _inventory.get(isbn)
    if not book:
        return False
    book['stock'] += qty
    return True


def list_inventory():
    return deepcopy(list(_inventory.values()))
