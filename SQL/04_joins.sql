
-- =====================================================
-- PROJECT: NovaCart E-Commerce Analytics
-- FILE: 04_joins.sql
-- PURPOSE: Combine related tables using SQL JOINs
-- =====================================================

USE novacart;

-- 1. INNER JOIN: Orders with product details
SELECT
    o.order_id,
    o.product_id,
    p.product_name,
    p.category,
    o.quantity,
    o.net_revenue
FROM orders AS o
INNER JOIN products AS p
    ON o.product_id = p.product_id
LIMIT 20;

-- 2. LEFT JOIN: Keep all orders and show return details
SELECT
    o.order_id,
    o.order_date,
    o.customer_id,
    r.return_id,
    r.return_date,
    r.return_reason
FROM orders AS o
LEFT JOIN returns AS r
    ON o.order_id = r.order_id
LIMIT 20;

-- 3. INNER JOIN: Customer details with their orders
SELECT
    c.customer_id,
    c.customer_name,
    c.region,
    o.order_id,
    o.order_date,
    o.net_revenue
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
LIMIT 20;

-- 4. Category-level revenue
SELECT
    p.category,
    ROUND(SUM(o.net_revenue), 2) AS total_revenue
FROM orders AS o
INNER JOIN products AS p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- 5. Category-level revenue, profit and profit margin
SELECT
    p.category,
    ROUND(SUM(o.net_revenue), 2) AS total_revenue,
    ROUND(SUM(o.profit), 2) AS total_profit,
    ROUND(
        SUM(o.profit) / NULLIF(SUM(o.net_revenue), 0) * 100,
        2
    ) AS profit_margin_percent
FROM orders AS o
INNER JOIN products AS p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- 6. Return rate by product category
SELECT
    p.category,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT r.order_id) AS returned_orders,
    ROUND(
        COUNT(DISTINCT r.order_id)
        / NULLIF(COUNT(DISTINCT o.order_id), 0) * 100,
        2
    ) AS return_rate_percent
FROM orders AS o
INNER JOIN products AS p
    ON o.product_id = p.product_id
LEFT JOIN returns AS r
    ON o.order_id = r.order_id
GROUP BY p.category
ORDER BY return_rate_percent DESC;
