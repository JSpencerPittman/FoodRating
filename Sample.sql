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
INSERT INTO site (company_no, state, street, address, zip) VALUES
(1, 'California', 'Main St', '123 Main St', '90001'),
(2, 'New York', 'Broadway', '456 Broadway Ave', '10001'),
(1, 'Texas', 'Elm St', '789 Elm St', '75001'),
(4, 'Washington', 'Pine St', '101 Pine St', '98001'),
(1, 'Florida', 'Ocean Dr', '202 Ocean Dr', '33139');

-- Populate Foods
INSERT INTO food (company_no, food_name, cuisine) VALUES
(1, '5 Layer Burrito', 'Mexican'),
(1, 'Chalupa', 'Mexican'),
(2, 'Lobster', NULL),
(5, 'Gravy', 'American'),
(5, 'Kernel Chicken', 'American');


-- RESET DELETE THIS
DROP TABLE site CASCADE;
DROP TABLE customer CASCADE;
DROP TABLE company CASCADE;