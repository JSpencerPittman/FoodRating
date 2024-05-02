--- Populate Customers
INSERT INTO customer (email, psswd, fname, mname, lname) VALUES
('alice@example.com', 'password123', 'Alice', 'B.', 'Smith'),
('bob@example.com', 'password456', 'Bob', 'C.', 'Jones'),
('carol@example.com', 'password789', 'Carol', 'D.', 'Brown'),
('david@example.com', 'password101', 'David', 'E.', 'Wilson'),
('eve@example.com', 'password202', 'Eve', 'F.', 'Taylor');

-- Populate Companies
INSERT INTO company (comp_name, comp_type) VALUES
('Taco Bell', 'Fast Food'),
('Red Lobster', 'Restaurant'),
('McDonalds', 'Fast Food'),
('Starbucks', NULL),
('KFC', 'Fast Food');

-- Populate Sites
INSERT INTO site (company_id, state, street, addr_num, zip) VALUES
(1, 'California', 'Main St', 123, 90001),
(2, 'New York', 'Broadway', 456, 10001),
(1, 'Texas', 'Elm St', 789, 75001),
(4, 'Washington', 'Pine St', 101, 98001),
(3, 'Florida', 'Ocean Dr', 202, 33139),
(5, 'Florida', 'Franklin Blvd', 407, 33138);

-- Populate Foods
INSERT INTO food (company_id, food_name, cuisine) VALUES
(1, '5 Layer Burrito', 'Mexican'),
(1, 'Chalupa', 'Mexican'),
(2, 'Lobster', NULL),
(5, 'Gravy', 'American'),
(5, 'Kernel Chicken', 'American');

-- Populate Ratings
INSERT INTO rating (food_id, site_id, cust_id, price, rating) VALUES
(1, 1, 1, NULL, 4),
(1, 3, 2, 12.48, 3),
(1, 1, 3, 1.2, 2),
(2, 3, 1, 2.4, 1),
(3, 2, 2, NULL, 2),
(4, 6, 3, NULL, 4),
(4, 6, 4, 4.32, 5),
(5, 6, 5, 4.21, 3);