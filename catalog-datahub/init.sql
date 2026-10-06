CREATE TABLE customers (id INT PRIMARY KEY, email TEXT NOT NULL, country TEXT);
CREATE TABLE orders (id INT PRIMARY KEY, customer_id INT REFERENCES customers(id), amount NUMERIC(10,2));
COMMENT ON TABLE customers IS 'Customer master data, owned by the sales team';
COMMENT ON TABLE orders IS 'Customer orders, owned by the sales team';
COMMENT ON COLUMN customers.email IS 'PII';
