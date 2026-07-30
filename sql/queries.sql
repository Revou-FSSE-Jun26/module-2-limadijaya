-- 1. Find the top 3 most expensive in-stock products under the 'Electronics' category (ID 1)
-- Demonstrates WHERE, ORDER BY, and LIMIT combined
SELECT 
    id, 
    name, 
    price, 
    stock_quantity 
FROM products
WHERE category_id = 1 AND stock_quantity > 0
ORDER BY price DESC
LIMIT 3;