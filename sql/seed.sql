-- Seed Categories
INSERT INTO categories (name, description) VALUES
('Electronics', 'Gadgets, devices, and accessories'),
('Apparel', 'Clothing, footwear, and accessories'),
('Home & Kitchen', 'Furniture, cookware, and appliances');

-- Seed Users
INSERT INTO users (full_name, email, password_hash) VALUES
('Alice Smith', 'alice@example.com', '$2b$12$hashedpasswordalice'),
('Bob Jones', 'bob@example.com', '$2b$12$hashedpasswordbob'),
('Charlie Brown', 'charlie@example.com', '$2b$12$hashedpasswordcharlie');

-- Seed Products
INSERT INTO products (category_id, name, description, price, stock_quantity) VALUES
(1, 'Wireless Noise-Canceling Headphones', 'High quality audio over-ear headphones', 199.99, 50),
(1, 'Mechanical Gaming Keyboard', 'RGB backlight with blue switches', 89.50, 100),
(2, 'Classic Cotton T-Shirt', '100% organic cotton unisex tee', 24.99, 200),
(2, 'Denim Jacket', 'Vintage style denim jacket', 79.99, 30),
(3, 'Stainless Steel French Press', '1 Liter capacity coffee maker', 34.95, 45);

-- Seed Orders
INSERT INTO orders (user_id, status, total_amount) VALUES
(1, 'completed', 224.98),
(2, 'shipped', 79.99),
(1, 'pending', 34.95);

-- Seed Order Items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 199.99),
(1, 3, 1, 24.99),
(2, 4, 1, 79.99),
(3, 5, 1, 34.95);