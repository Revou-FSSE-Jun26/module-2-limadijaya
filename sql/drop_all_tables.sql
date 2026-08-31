-- =====================================================================
-- DESTRUCTIVE: Drops all RevoShop tables and data.
-- Run this only if you want to start the schema completely from scratch.
-- There is no undo unless you have a backup/snapshot.
--
-- Order matters: drop dependent tables (order_items) before the tables
-- they reference (orders, products), etc. CASCADE handles any leftover
-- foreign key dependencies automatically.
-- =====================================================================

DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Also clear Alembic's migration tracking, since the tables it was
-- tracking no longer exist. Otherwise `flask db upgrade` will think
-- the migration already ran and skip recreating anything.
DROP TABLE IF EXISTS alembic_version CASCADE;
