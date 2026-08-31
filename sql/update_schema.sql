-- =====================================================================
-- Update script: aligns an existing Supabase database (created from the
-- OLD schema.sql with full_name and CHECK constraints) with the current
-- models.py / migration state.
--
-- Safe to run once. Wrapped in a transaction so it's all-or-nothing.
-- Run this in the Supabase SQL Editor.
-- =====================================================================

BEGIN;

-- ---------------------------------------------------------------------
-- 1. USERS: add username + role, backfill username, drop full_name
-- ---------------------------------------------------------------------

-- Add the new columns as nullable first (so existing rows don't error)
ALTER TABLE users ADD COLUMN IF NOT EXISTS username VARCHAR(80);
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) NOT NULL DEFAULT 'customer';

-- Backfill username from full_name for any existing rows
UPDATE users SET username = full_name WHERE username IS NULL;

-- Now that every row has a value, enforce NOT NULL
ALTER TABLE users ALTER COLUMN username SET NOT NULL;

-- Drop the old column
ALTER TABLE users DROP COLUMN IF EXISTS full_name;

-- ---------------------------------------------------------------------
-- 2. PRODUCTS: drop CHECK constraints (validation now handled in Flask)
-- ---------------------------------------------------------------------

ALTER TABLE products DROP CONSTRAINT IF EXISTS products_price_check;
ALTER TABLE products DROP CONSTRAINT IF EXISTS products_stock_quantity_check;

-- ---------------------------------------------------------------------
-- 3. ORDER_ITEMS: drop CHECK constraints + add default quantity
-- ---------------------------------------------------------------------

ALTER TABLE order_items DROP CONSTRAINT IF EXISTS order_items_quantity_check;
ALTER TABLE order_items DROP CONSTRAINT IF EXISTS order_items_unit_price_check;
ALTER TABLE order_items ALTER COLUMN quantity SET DEFAULT 1;

COMMIT;

-- =====================================================================
-- Verification queries (run separately after COMMIT to confirm)
-- =====================================================================
-- SELECT column_name, data_type, is_nullable, column_default
--   FROM information_schema.columns WHERE table_name = 'users';
--
-- SELECT conname FROM pg_constraint
--   WHERE conrelid = 'products'::regclass OR conrelid = 'order_items'::regclass;
