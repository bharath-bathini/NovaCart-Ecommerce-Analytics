
-- =====================================================
-- PROJECT: NovaCart E-Commerce Analytics
-- FILE: 01_database_setup.sql
-- PURPOSE: Create and select the project database
-- DATABASE: MySQL 8.0
-- =====================================================

CREATE DATABASE IF NOT EXISTS novacart;

USE novacart;

-- Confirm that the correct database is selected
SELECT DATABASE();

-- Display the tables currently in the database
SHOW TABLES;
