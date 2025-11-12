"""Create a sample source SQLite DB representing the Customer Data System.
This simulates an existing relational customer DB (customers_source.db).
"""
import sqlite3

DB_PATH = 'customers_source.db'

customers = [
    # customer_id, name, street, city, email, phone
    (1, 'Alice Johnson', '12 Baker St', 'Nairobi', 'alice.j@example.com', '+254700111222'),
    (2, 'Bob Kamau', '45 River Rd', 'Mombasa', 'bob.k@example.com', '+254700333444'),
    (3, 'Carol Otieno', '7 Market Lane', 'Kisumu', 'carol.o@example.com', '+254700555666'),
    # a duplicate-ish record to show dedupe handling
    (4, 'Alice Johnson', '12 Baker St', 'Nairobi', 'alice.johnson@example.com', '+254700111222')
]

if __name__ == '__main__':
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        address_street TEXT,
        address_city TEXT,
        email TEXT,
        phone TEXT
    )''')
    cur.executemany('INSERT OR REPLACE INTO customers (customer_id, full_name, address_street, address_city, email, phone) VALUES (?,?,?,?,?,?)', customers)
    conn.commit()
    conn.close()
    print(f'Created {DB_PATH} with {len(customers)} customers')
