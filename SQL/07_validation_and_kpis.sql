
-- ============================================================
-- PROJECT: NovaCart E-Commerce Analytics
-- FILE: 07_validation_and_kpis.sql
-- PURPOSE: Data validation and key business KPI calculations
-- DATABASE: novacart
-- ============================================================

USE novacart;

-- ============================================================
-- SECTION 1: VALIDATE TABLE ROW COUNTS
-- Expected counts: customers 5000, products 200,
-- orders 50000, returns 4000
-- ============================================================

SELECT 'customers' AS table_name, COUNT(*) AS row_count
FROM customers
UNION ALL
SELECT 'products', COUNT(*)
FROM products
UNION ALL
SELECT 'orders', COUNT(*)
FROM orders
UNION ALL
SELECT 'returns', COUNT(*)
FROM returns;


-- ============================================================
-- SECTION 2: CHECK PRIMARY IDENTIFIERS FOR DUPLICATES
-- Each identifier should normally be unique.
-- These queries should return zero rows.
-- ============================================================

SELECT customer_id, COUNT(*) AS duplicate_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

SELECT product_id, COUNT(*) AS duplicate_count
FROM products
GROUP BY product_id
HAVING COUNT(*) > 1;

SELECT order_id, COUNT(*) AS duplicate_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;

SELECT return_id, COUNT(*) AS duplicate_count
FROM returns
GROUP BY return_id
HAVING COUNT(*) > 1;


-- ============================================================
-- SECTION 3: CHECK MISSING IMPORTANT VALUES
-- ============================================================

SELECT
    SUM(customer_id IS NULL) AS missing_customer_ids,
    SUM(customer_name IS NULL) AS missing_customer_names,
    SUM(region IS NULL) AS missing_regions
FROM customers;

SELECT
    SUM(product_id IS NULL) AS missing_product_ids,
    SUM(category IS NULL) AS missing_categories,
    SUM(selling_price IS NULL) AS missing_selling_prices
FROM products;

SELECT
    SUM(order_id IS NULL) AS missing_order_ids,
    SUM(order_date IS NULL) AS missing_order_dates,
    SUM(customer_id IS NULL) AS missing_order_customer_ids,
    SUM(product_id IS NULL) AS missing_order_product_ids,
    SUM(net_revenue IS NULL) AS missing_net_revenue,
    SUM(profit IS NULL) AS missing_profit
FROM orders;


-- ============================================================
-- SECTION 4: CHECK ORPHANED FOREIGN KEYS
-- Each query should return zero rows.
-- ============================================================

-- Orders with no matching customer
SELECT o.order_id, o.customer_id
FROM orders AS o
LEFT JOIN customers AS c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Orders with no matching product
SELECT o.order_id, o.product_id
FROM orders AS o
LEFT JOIN products AS p
    ON o.product_id = p.product_id
WHERE p.product_id IS NULL;

-- Returns with no matching order
SELECT r.return_id, r.order_id
FROM returns AS r
LEFT JOIN orders AS o
    ON r.order_id = o.order_id
WHERE o.order_id IS NULL;


-- ============================================================
-- SECTION 5: CHECK BUSINESS RULES
-- Investigate any rows returned by these queries.
-- ============================================================

-- Invalid quantities
SELECT *
FROM orders
WHERE quantity IS NULL OR quantity <= 0;

-- Discounts outside the expected 0–0.30 range
SELECT *
FROM orders
WHERE discount IS NULL OR discount < 0 OR discount > 0.30;

-- Selling price below cost price
SELECT *
FROM products
WHERE selling_price < cost_price;

-- Net revenue should not exceed gross sales
SELECT *
FROM orders
WHERE net_revenue > gross_sales;

-- Returns dated before their orders or more than 30 days later
SELECT
    r.return_id,
    r.order_id,
    o.order_date,
    r.return_date,
    DATEDIFF(r.return_date, o.order_date) AS return_delay_days
FROM returns AS r
JOIN orders AS o
    ON r.order_id = o.order_id
WHERE r.return_date < o.order_date
   OR DATEDIFF(r.return_date, o.order_date) NOT BETWEEN 1 AND 30;


-- ============================================================
-- SECTION 6: EXECUTIVE BUSINESS KPIs
-- ============================================================

SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS purchasing_customers,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(gross_sales), 2) AS gross_sales,
    ROUND(SUM(net_revenue), 2) AS net_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(profit_margin), 2) AS average_order_row_margin_percent,
    ROUND(
        100.0 * SUM(profit) / NULLIF(SUM(net_revenue), 0),
        2
    ) AS overall_profit_margin_percent
FROM orders;


-- ============================================================
-- SECTION 7: AVERAGE ORDER VALUE
-- ============================================================

SELECT
    ROUND(SUM(net_revenue) / NULLIF(COUNT(DISTINCT order_id), 0), 2)
        AS average_order_value
FROM orders;


-- ============================================================
-- SECTION 8: RETURN KPIs
-- Uses distinct returned order IDs to avoid double counting.
-- ============================================================

SELECT
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT r.order_id) AS returned_orders,
    ROUND(
        100.0 * COUNT(DISTINCT r.order_id)
        / NULLIF(COUNT(DISTINCT o.order_id), 0),
        2
    ) AS return_rate_percent
FROM orders AS o
LEFT JOIN returns AS r
    ON o.order_id = r.order_id;


-- ============================================================
-- SECTION 9: YEARLY REVENUE AND PROFIT
-- ============================================================

SELECT
    YEAR(order_date) AS order_year,
    COUNT(*) AS total_orders,
    ROUND(SUM(net_revenue), 2) AS net_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(
        100.0 * SUM(profit) / NULLIF(SUM(net_revenue), 0),
        2
    ) AS profit_margin_percent
FROM orders
GROUP BY YEAR(order_date)
ORDER BY order_year;


-- ============================================================
-- SECTION 10: CATEGORY PERFORMANCE
-- ============================================================

SELECT
    p.category,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.net_revenue), 2) AS net_revenue,
    ROUND(SUM(o.profit), 2) AS total_profit,
    ROUND(
        100.0 * SUM(o.profit) / NULLIF(SUM(o.net_revenue), 0),
        2
    ) AS profit_margin_percent
FROM orders AS o
JOIN products AS p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY net_revenue DESC;


-- ============================================================
-- SECTION 11: REGION PERFORMANCE
-- ============================================================

SELECT
    c.region,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS purchasing_customers,
    ROUND(SUM(o.net_revenue), 2) AS net_revenue,
    ROUND(SUM(o.profit), 2) AS total_profit
FROM orders AS o
JOIN customers AS c
    ON o.customer_id = c.customer_id
GROUP BY c.region
ORDER BY net_revenue DESC;


-- ============================================================
-- SECTION 12: RETURN REASONS
-- ============================================================

SELECT
    return_reason,
    COUNT(*) AS return_count
FROM returns
GROUP BY return_reason
ORDER BY return_count DESC;
