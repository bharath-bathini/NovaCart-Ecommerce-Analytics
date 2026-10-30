
-- =====================================================
-- PROJECT: NovaCart E-Commerce Analytics
-- FILE: 05_business_analysis.sql
-- PURPOSE: Answer business questions using SQL
-- =====================================================

USE novacart;

-- 1. Top 10 products by net revenue
SELECT
    p.product_id,
    p.product_name,
    p.category,
    ROUND(SUM(o.net_revenue), 2) AS total_revenue
FROM orders AS o
JOIN products AS p
    ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;

-- 2. Revenue and profit by category
SELECT
    p.category,
    ROUND(SUM(o.net_revenue), 2) AS total_revenue,
    ROUND(SUM(o.profit), 2) AS total_profit
FROM orders AS o
JOIN products AS p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- 3. Yearly revenue and profit
SELECT
    YEAR(order_date) AS order_year,
    ROUND(SUM(net_revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY YEAR(order_date)
ORDER BY order_year;

-- 4. Monthly revenue and profit
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS order_month,
    ROUND(SUM(net_revenue), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY order_month;

-- 5. Revenue and profit by customer region
SELECT
    c.region,
    ROUND(SUM(o.net_revenue), 2) AS total_revenue,
    ROUND(SUM(o.profit), 2) AS total_profit,
    ROUND(
        SUM(o.profit) / NULLIF(SUM(o.net_revenue), 0) * 100,
        2
    ) AS profit_margin_percent
FROM orders AS o
JOIN customers AS c
    ON o.customer_id = c.customer_id
GROUP BY c.region
ORDER BY total_revenue DESC;

-- 6. Most common return reasons
SELECT
    return_reason,
    COUNT(*) AS return_count
FROM returns
GROUP BY return_reason
ORDER BY return_count DESC;

-- 7. Top 10 customers by net revenue
SELECT
    c.customer_id,
    c.customer_name,
    c.region,
    ROUND(SUM(o.net_revenue), 2) AS total_revenue
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.region
ORDER BY total_revenue DESC
LIMIT 10;

-- 8. Count repeat customers
SELECT
    COUNT(*) AS repeat_customers
FROM (
    SELECT customer_id
    FROM orders
    GROUP BY customer_id
    HAVING COUNT(DISTINCT order_id) > 1
) AS repeat_customer_list;

-- 9. Top 10 products by total profit
SELECT
    p.product_id,
    p.product_name,
    p.category,
    ROUND(SUM(o.profit), 2) AS total_profit,
    ROUND(SUM(o.net_revenue), 2) AS total_revenue
FROM orders AS o
JOIN products AS p
    ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_profit DESC
LIMIT 10;

-- 10. Find products with negative total profit
SELECT
    p.product_id,
    p.product_name,
    p.category,
    ROUND(SUM(o.net_revenue), 2) AS total_revenue,
    ROUND(SUM(o.profit), 2) AS total_profit,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM orders AS o
JOIN products AS p
    ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
HAVING SUM(o.profit) < 0
ORDER BY total_profit ASC;

-- 11. Count loss-making products and calculate their combined loss
SELECT
    COUNT(*) AS loss_making_products,
    ROUND(SUM(product_profit), 2) AS combined_product_loss,
    ROUND(AVG(product_profit), 2) AS average_loss_per_product
FROM (
    SELECT
        product_id,
        SUM(profit) AS product_profit
    FROM orders
    GROUP BY product_id
    HAVING SUM(profit) < 0
) AS loss_products;

-- 12. Return rate by category
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
JOIN products AS p
    ON o.product_id = p.product_id
LEFT JOIN returns AS r
    ON o.order_id = r.order_id
GROUP BY p.category
ORDER BY return_rate_percent DESC;
