"""Modern, typed in-memory inventory mock.

This module uses simple dataclasses and type hints for clearer structure
and easier maintenance. Data remains in-memory for the demo.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from copy import deepcopy
from threading import Lock


@dataclass
class Book:
    isbn: str
    title: str
    author: str
    price: float
    stock: int


# internal storage and lock for thread-safety
_inventory: Dict[str, Book] = {
    '9780143127550': Book('9780143127550', 'The Martian', 'Andy Weir', 12.99, 10),
    '9780262033848': Book('9780262033848', 'Introduction to Algorithms', 'Cormen et al.', 89.99, 3),
    '9780140449136': Book('9780140449136', 'The Odyssey', 'Homer', 9.50, 25),
}
_lock = Lock()


def get_book(isbn: str) -> Optional[dict]:
    with _lock:
        b = _inventory.get(isbn)
        return deepcopy(asdict(b)) if b else None


def reserve_stock(isbn: str, qty: int) -> tuple[bool, Optional[str]]:
    """Reserve `qty` units of `isbn`. Returns (success, error_message).
    Thread-safe and atomic for the in-memory store.
    """
    with _lock:
        b = _inventory.get(isbn)
        if not b:
            return False, 'Book not found'
        if b.stock < qty:
            return False, 'Insufficient stock'
        b.stock -= qty
        return True, None


def replenish_stock(isbn: str, qty: int) -> bool:
    with _lock:
        b = _inventory.get(isbn)
        if not b:
            return False
        b.stock += qty
        return True


def list_inventory() -> List[dict]:
    with _lock:
        return deepcopy([asdict(b) for b in _inventory.values()])
