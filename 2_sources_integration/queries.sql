-- Queries demonstrating integrated data retrieval

-- 1) Fetch customer details along with the products they ordered (flattened view)
SELECT o.order_id, o.order_date, c.customer_id, c.full_name, p.product_id, p.product_name, oi.quantity, oi.unit_price, oi.line_total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
ORDER BY o.order_date;

-- 2) Calculate total value of orders per customer
SELECT c.customer_id, c.full_name, SUM(o.total) AS total_spent, COUNT(o.order_id) AS order_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.full_name
ORDER BY total_spent DESC;

-- 3) Filter products by price range (example: between 900 and 5000)
SELECT product_id, product_name, price, stock FROM products WHERE price BETWEEN 900 AND 5000 ORDER BY price;

-- 4) Identify customers with orders exceeding a certain amount (e.g., total_spent > 5000)
WITH customer_totals AS (
  SELECT customer_id, SUM(total) AS total_spent
  FROM orders
  GROUP BY customer_id
)
SELECT c.customer_id, c.full_name, ct.total_spent
FROM customers c
JOIN customer_totals ct ON ct.customer_id = c.customer_id
WHERE ct.total_spent > 5000
ORDER BY ct.total_spent DESC;

-- 5) Report: total orders and revenue generated per product
SELECT p.product_id, p.product_name, SUM(oi.quantity) AS total_qty_sold, SUM(oi.line_total) AS revenue
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name
ORDER BY revenue DESC;
