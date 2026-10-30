
-- =====================================================
-- PROJECT: NovaCart E-Commerce Analytics
-- FILE: 06_advanced_sql.sql
-- PURPOSE: Subqueries, CTEs, date functions and windows
-- =====================================================

USE novacart;

-- 1. Subquery: products with revenue above average product revenue
SELECT
    product_id,
    total_revenue
FROM (
    SELECT
        product_id,
        SUM(net_revenue) AS total_revenue
    FROM orders
    GROUP BY product_id
) AS product_revenue
WHERE total_revenue > (
    SELECT AVG(product_total)
    FROM (
        SELECT SUM(net_revenue) AS product_total
        FROM orders
        GROUP BY product_id
    ) AS average_product_revenue
)
ORDER BY total_revenue DESC;

-- 2. CTE: top 10 products by revenue
WITH product_revenue AS (
    SELECT
        product_id,
        SUM(net_revenue) AS total_revenue
    FROM orders
    GROUP BY product_id
)
SELECT
    product_id,
    ROUND(total_revenue, 2) AS total_revenue
FROM product_revenue
ORDER BY total_revenue DESC
LIMIT 10;

-- 3. CTE: top 10 products by profit
WITH product_profit AS (
    SELECT
        product_id,
        SUM(profit) AS total_profit
    FROM orders
    GROUP BY product_id
)
SELECT
    product_id,
    ROUND(total_profit, 2) AS total_profit
FROM product_profit
ORDER BY total_profit DESC
LIMIT 10;

-- 4. Handle NULL values
SELECT *
FROM customers
WHERE region IS NULL;

SELECT *
FROM customers
WHERE region IS NOT NULL
LIMIT 10;

SELECT
    customer_id,
    COALESCE(region, 'Unknown') AS region
FROM customers
LIMIT 10;

-- 5. Count orders by year
SELECT
    YEAR(order_date) AS order_year,
    COUNT(*) AS order_count
FROM orders
GROUP BY YEAR(order_date)
ORDER BY order_year;

-- 6. Count orders by month number
SELECT
    MONTH(order_date) AS month_number,
    COUNT(*) AS order_count
FROM orders
GROUP BY MONTH(order_date)
ORDER BY month_number;

-- 7. Count orders by year and month
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS order_month,
    COUNT(*) AS order_count
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY order_month;

-- 8. ROW_NUMBER: rank products by revenue
WITH product_revenue AS (
    SELECT
        product_id,
        SUM(net_revenue) AS total_revenue
    FROM orders
    GROUP BY product_id
)
SELECT
    product_id,
    ROUND(total_revenue, 2) AS total_revenue,
    ROW_NUMBER() OVER (
        ORDER BY total_revenue DESC
    ) AS revenue_rank
FROM product_revenue
ORDER BY revenue_rank
LIMIT 10;

-- 9. RANK: ties share rank, with gaps after ties
WITH product_revenue AS (
    SELECT
        product_id,
        SUM(net_revenue) AS total_revenue
    FROM orders
    GROUP BY product_id
)
SELECT
    product_id,
    ROUND(total_revenue, 2) AS total_revenue,
    RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS revenue_rank
FROM product_revenue
ORDER BY revenue_rank
LIMIT 10;

-- 10. DENSE_RANK: ties share rank, without gaps
WITH product_revenue AS (
    SELECT
        product_id,
        SUM(net_revenue) AS total_revenue
    FROM orders
    GROUP BY product_id
)
SELECT
    product_id,
    ROUND(total_revenue, 2) AS total_revenue,
    DENSE_RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS revenue_rank
FROM product_revenue
ORDER BY revenue_rank
LIMIT 10;

-- 11. Rank products within each category
WITH product_revenue AS (
    SELECT
        p.category,
        p.product_id,
        p.product_name,
        SUM(o.net_revenue) AS total_revenue
    FROM orders AS o
    JOIN products AS p
        ON o.product_id = p.product_id
    GROUP BY p.category, p.product_id, p.product_name
),
ranked_products AS (
    SELECT
        category,
        product_id,
        product_name,
        total_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY total_revenue DESC
        ) AS category_rank
    FROM product_revenue
)
SELECT
    category,
    product_id,
    product_name,
    ROUND(total_revenue, 2) AS total_revenue,
    category_rank
FROM ranked_products
WHERE category_rank <= 3
ORDER BY category, category_rank;

-- 12. Rank customers within each region
WITH customer_revenue AS (
    SELECT
        c.region,
        c.customer_id,
        c.customer_name,
        SUM(o.net_revenue) AS total_revenue
    FROM customers AS c
    JOIN orders AS o
        ON c.customer_id = o.customer_id
    GROUP BY c.region, c.customer_id, c.customer_name
),
ranked_customers AS (
    SELECT
        region,
        customer_id,
        customer_name,
        total_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY region
            ORDER BY total_revenue DESC
        ) AS region_rank
    FROM customer_revenue
)
SELECT
    region,
    customer_id,
    customer_name,
    ROUND(total_revenue, 2) AS total_revenue,
    region_rank
FROM ranked_customers
WHERE region_rank <= 3
ORDER BY region, region_rank;

-- 13. Customer average order value (AOV)
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(o.net_revenue), 2) AS total_revenue,
    ROUND(
        SUM(o.net_revenue) / NULLIF(COUNT(DISTINCT o.order_id), 0),
        2
    ) AS customer_aov
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY customer_aov DESC
LIMIT 10;

-- 14. Historical customer value proxy
-- Note: this is historical revenue, not predictive customer lifetime value.
SELECT
    c.customer_id,
    c.customer_name,
    c.region,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.quantity) AS total_units,
    ROUND(SUM(o.net_revenue), 2) AS historical_customer_value
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.region
ORDER BY historical_customer_value DESC
LIMIT 10;
