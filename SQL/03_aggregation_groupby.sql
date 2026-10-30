
-- =====================================================
-- PROJECT: NovaCart E-Commerce Analytics
-- FILE: 03_aggregation_groupby.sql
-- PURPOSE: Aggregations, GROUP BY, HAVING and CASE
-- =====================================================

USE novacart;

-- 1. Count all customers
SELECT COUNT(*) AS total_customers
FROM customers;

-- 2. Calculate total units sold
SELECT SUM(quantity) AS total_units_sold
FROM orders;

-- 3. Calculate average quantity per order row
SELECT ROUND(AVG(quantity), 4) AS average_quantity
FROM orders;

-- 4. Find minimum and maximum quantities
SELECT
    MIN(quantity) AS minimum_quantity,
    MAX(quantity) AS maximum_quantity
FROM orders;

-- 5. Count customers in each region
SELECT
    region,
    COUNT(*) AS customer_count
FROM customers
GROUP BY region
ORDER BY customer_count DESC;

-- 6. Calculate units sold by payment method
SELECT
    payment_method,
    SUM(quantity) AS total_units
FROM orders
GROUP BY payment_method
ORDER BY total_units DESC;

-- 7. Find average quantity by payment method
SELECT
    payment_method,
    ROUND(AVG(quantity), 4) AS average_quantity
FROM orders
GROUP BY payment_method
ORDER BY average_quantity DESC;

-- 8. Use HAVING to keep groups with average quantity above 3.01
SELECT
    payment_method,
    ROUND(AVG(quantity), 4) AS average_quantity
FROM orders
GROUP BY payment_method
HAVING AVG(quantity) > 3.01;

-- 9. Filter rows first, then group and filter groups
SELECT
    payment_method,
    SUM(quantity) AS total_quantity
FROM orders
WHERE quantity > 2
GROUP BY payment_method
HAVING SUM(quantity) > 20000
ORDER BY total_quantity DESC;

-- 10. Classify customers by age
SELECT
    customer_id,
    customer_name,
    age,
    CASE
        WHEN age < 25 THEN 'Young'
        WHEN age BETWEEN 25 AND 40 THEN 'Adult'
        ELSE 'Senior'
    END AS age_category
FROM customers
LIMIT 10;

-- 11. Count customers in each age category
SELECT
    CASE
        WHEN age < 25 THEN 'Young'
        WHEN age BETWEEN 25 AND 40 THEN 'Adult'
        ELSE 'Senior'
    END AS age_category,
    COUNT(*) AS customer_count
FROM customers
GROUP BY age_category
ORDER BY customer_count DESC;
