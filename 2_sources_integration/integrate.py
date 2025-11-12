"""Integration script
- Reads customers from customers_source.db (SQLite)
- Reads products from products.csv
- Writes into central.db with schema from schema.sql
- Demonstrates simple deduplication and validation
"""
import sqlite3
import csv
import os
from datetime import datetime

SOURCE_DB = 'customers_source.db'
PRODUCTS_CSV = 'products.csv'
CENTRAL_DB = 'central.db'

# Simple dedupe helper: prefer existing id, otherwise insert as new

def load_customers(src_conn, central_conn):
    src_cur = src_conn.cursor()
    dst_cur = central_conn.cursor()
    src_cur.execute('SELECT customer_id, full_name, address_street, address_city, email, phone FROM customers')
    rows = src_cur.fetchall()
    inserted = 0
    for r in rows:
        cid, name, street, city, email, phone = r
        # Basic validation: require name
        if not name:
            print(f'Skipping customer {cid} due to missing name')
            continue
        # Try to find existing customer by email or phone
        dst_cur.execute('SELECT customer_id FROM customers WHERE email = ? OR phone = ?', (email, phone))
        found = dst_cur.fetchone()
        if found:
            # update record with any missing fields
            existing_id = found[0]
            dst_cur.execute('''UPDATE customers SET full_name = COALESCE(full_name, ?), address_street = COALESCE(address_street, ?), address_city = COALESCE(address_city, ?), email = COALESCE(email, ?), phone = COALESCE(phone, ?) WHERE customer_id = ?''', (name, street, city, email, phone, existing_id))
        else:
            dst_cur.execute('INSERT INTO customers (customer_id, full_name, address_street, address_city, email, phone, created_at) VALUES (?,?,?,?,?,?,?)', (cid, name, street, city, email, phone, datetime.utcnow().isoformat()))
            inserted += 1
    central_conn.commit()
    print(f'Customers loaded/merged. Inserted: {inserted}')


def load_products(csv_path, central_conn):
    dst_cur = central_conn.cursor()
    inserted = 0
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            # validation
            try:
                pid = int(r['product_id'])
                name = r['product_name']
                price = float(r['price'])
                stock = int(r.get('stock') or 0)
            except Exception as e:
                print('Skipping product row due to parse error:', r, e)
                continue
            # upsert pattern for SQLite
            dst_cur.execute('SELECT product_id FROM products WHERE product_id=?', (pid,))
            if dst_cur.fetchone():
                dst_cur.execute('UPDATE products SET product_name=?, price=?, stock=?, created_at=CURRENT_TIMESTAMP WHERE product_id=?', (name, price, stock, pid))
            else:
                dst_cur.execute('INSERT INTO products (product_id, product_name, price, stock, created_at) VALUES (?,?,?,?,?)', (pid, name, price, stock, datetime.utcnow().isoformat()))
                inserted += 1
    central_conn.commit()
    print(f'Products loaded. Inserted: {inserted}')


def create_sample_orders(central_conn):
    cur = central_conn.cursor()
    # Create a couple of sample orders linking customers and products
    orders = [
        # customer_id, [(product_id, qty), ...]
        (1, [(1002, 2), (1004, 1)]),
        (2, [(1001, 1), (1005, 1)]),
        (3, [(1003, 3)]),
        # an order by the deduped Alice (id 4 originally) — will match by phone/email to id 1
        (4, [(1002, 1)])
    ]
    for cust_id, items in orders:
        # verify customer exists
        cur.execute('SELECT customer_id FROM customers WHERE customer_id=? OR email IN (SELECT email FROM customers WHERE phone=(SELECT phone FROM customers WHERE customer_id=?))', (cust_id, cust_id))
        if not cur.fetchone():
            print(f'Customer {cust_id} missing in central DB — skipping order')
            continue
        cur.execute('INSERT INTO orders (customer_id, order_date, total) VALUES (?, ?, ?)', (cust_id, datetime.utcnow().isoformat(), 0))
        order_id = cur.lastrowid
        total = 0
        for pid, qty in items:
            cur.execute('SELECT price FROM products WHERE product_id=?', (pid,))
            row = cur.fetchone()
            if not row:
                print(f'Product {pid} not found — skipping line')
                continue
            unit_price = row[0]
            line_total = unit_price * qty
            cur.execute('INSERT INTO order_items (order_id, product_id, quantity, unit_price, line_total) VALUES (?,?,?,?,?)', (order_id, pid, qty, unit_price, line_total))
            total += line_total
        cur.execute('UPDATE orders SET total=? WHERE order_id=?', (total, order_id))
    central_conn.commit()
    print('Sample orders created')


if __name__ == '__main__':
    # create central DB and schema
    conn = sqlite3.connect(CENTRAL_DB)
    cur = conn.cursor()
    # enable foreign keys
    cur.execute('PRAGMA foreign_keys = ON')
    # execute schema
    if os.path.exists('schema.sql'):
        with open('schema.sql', 'r', encoding='utf-8') as f:
            sql = f.read()
            cur.executescript(sql)
    else:
        print('schema.sql not found')
        conn.close()
        raise SystemExit(1)

    # prepare source
    if not os.path.exists(SOURCE_DB):
        print(f'{SOURCE_DB} not found — run create_source_db.py first')
        conn.close()
        raise SystemExit(1)
    src_conn = sqlite3.connect(SOURCE_DB)

    load_customers(src_conn, conn)
    load_products(PRODUCTS_CSV, conn)
    create_sample_orders(conn)

    src_conn.close()
    conn.close()
    print(f'Integration complete. Central DB: {CENTRAL_DB}')
