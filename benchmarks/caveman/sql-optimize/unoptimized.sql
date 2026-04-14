/* 
  ENTERPRISE ANALYTICS QUERY
  Task: Optimize performance for a legacy reporting dashboard.
  Issues: SELECT *, Unfiltered Joins, Lack of Window Function optimization.
*/

EXPLAIN ANALYZE
SELECT 
    c.id AS customer_id,
    c.first_name || ' ' || c.last_name AS full_name,
    c.email,
    o.id AS order_id,
    o.order_date,
    o.total_amount,
    p.product_name,
    p.sku,
    cat.category_name,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS line_item_total,
    -- Inefficient way to get running totals per customer
    (SELECT SUM(total_amount) FROM orders WHERE customer_id = c.id AND order_date <= o.order_date) AS running_total_spend
FROM customers c
INNER JOIN orders o ON c.id = o.customer_id
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
INNER JOIN categories cat ON p.category_id = cat.id
LEFT JOIN promotions pr ON o.promotion_id = pr.id
WHERE o.order_date >= '2023-01-01'
  AND o.status NOT IN ('cancelled', 'returned')
  AND cat.category_name IN ('Electronics', 'Professional Services', 'Cloud Infrastructure')
  -- Heavy filter that might benefit from better indexing
  AND c.last_sign_in < NOW() - INTERVAL '30 days'
ORDER BY o.order_date DESC, c.id ASC
LIMIT 1000;
