CREATE TABLE IF NOT EXISTS customers (
    id INTEGER, name VARCHAR, email VARCHAR,
    city VARCHAR, signup_date DATE, is_premium BOOLEAN
);
INSERT INTO customers VALUES
    (1, 'Alice Johnson', 'alice@example.com', 'New York', '2024-01-15', true),
    (2, 'Bob Smith', 'bob@example.com', 'San Francisco', '2024-02-20', false),
    (3, 'Carol White', 'carol@example.com', 'Boston', '2024-01-10', true),
    (4, 'David Brown', 'david@example.com', 'Seattle', '2024-03-05', false),
    (5, 'Eve Davis', 'eve@example.com', 'Austin', '2024-02-28', true);
