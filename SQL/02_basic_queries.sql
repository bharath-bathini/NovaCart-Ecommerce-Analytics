
-- =====================================================
-- PROJECT: NovaCart E-Commerce Analytics
-- FILE: 02_basic_queries.sql
-- PURPOSE: Practise basic SQL queries
-- =====================================================

USE novacart;

-- 1. Display the first five customers
SELECT *
FROM customers
LIMIT 5;

-- 2. Select specific customer columns
SELECT customer_id, customer_name, age, region
FROM customers
LIMIT 10;

-- 3. Filter customers from the South region
SELECT *
FROM customers
WHERE region = 'South';

-- 4. Combine conditions using AND
SELECT customer_id, customer_name, age, region
FROM customers
WHERE region = 'South'
  AND age > 30;

-- 5. Combine conditions using OR
SELECT customer_id, customer_name, region
FROM customers
WHERE region = 'South'
   OR region = 'North';

-- 6. Exclude customers from the South region
SELECT customer_id, customer_name, region
FROM customers
WHERE region <> 'South';

-- 7. Find all distinct customer regions
SELECT DISTINCT region
FROM customers;

-- 8. Find all distinct payment methods
SELECT DISTINCT payment_method
FROM orders;

-- 9. Sort customers by age, oldest first
SELECT customer_id, customer_name, age
FROM customers
ORDER BY age DESC;

-- 10. Find the ten oldest customers
SELECT customer_id, customer_name, age
FROM customers
ORDER BY age DESC
LIMIT 10;

-- 11. Combined query: South region, older than 30
SELECT customer_id, customer_name, age, region
FROM customers
WHERE region = 'South'
  AND age > 30
ORDER BY age DESC
LIMIT 10;
