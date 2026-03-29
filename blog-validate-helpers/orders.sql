CREATE TABLE IF NOT EXISTS orders (
    id INTEGER, customer_id INTEGER, product VARCHAR,
    amount DECIMAL(10, 2), order_date DATE
);
INSERT INTO orders VALUES
    (1001, 1, 'Widget', 150.50, '2024-03-01'),
    (1002, 2, 'Gadget', 75.00, '2024-03-02'),
    (1003, 1, 'Gizmo', 200.00, '2024-03-05'),
    (1004, 3, 'Widget', 50.25, '2024-03-06'),
    (1005, 4, 'Doohickey', 300.00, '2024-03-07'),
    (1006, 1, 'Widget', 10.00, '2024-03-08'),
    (1007, 1, 'Widget', 500.00, '2024-03-09'),
    (1008, 1, 'Widget', 400.00, '2024-03-10'),
    (1009, 1, 'Widget', 600.00, '2024-03-11'),
    (1010, 1, 'Widget', 700.00, '2024-03-12');
