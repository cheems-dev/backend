-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS burger_orders;
USE burger_orders;
-- Create tables
CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  unit_price FLOAT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_number VARCHAR(50) NOT NULL UNIQUE,
  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(20) DEFAULT 'Pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS order_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL DEFAULT 1,
  unit_price FLOAT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);
-- Insert sample products
INSERT INTO products (name, unit_price)
VALUES ('Classic Burger', 9.99),
  ('Cheese Burger', 11.99),
  ('Bacon Burger', 12.99),
  ('Veggie Burger', 10.99),
  ('Double Burger', 14.99),
  ('Chicken Burger', 11.99),
  ('Fish Burger', 12.99),
  ('BBQ Burger', 13.99),
  ('Mushroom Burger', 12.99),
  ('Spicy Burger', 12.99);
-- Insert sample orders
INSERT INTO orders (order_number, status)
VALUES ('ORD-001', 'Completed'),
  ('ORD-002', 'InProgress'),
  ('ORD-003', 'Pending');
-- Insert sample order items
-- Order 1 items
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (1, 1, 2, 9.99),
  (1, 3, 1, 12.99);
-- Order 2 items
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (2, 2, 1, 11.99),
  (2, 5, 1, 14.99),
  (2, 8, 2, 13.99);
-- Order 3 items
INSERT INTO order_items (order_id, product_id, quantity, unit_price)
VALUES (3, 4, 1, 10.99),
  (3, 6, 1, 11.99);