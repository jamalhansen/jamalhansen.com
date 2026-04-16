CREATE TABLE IF NOT EXISTS deals (
    id INTEGER PRIMARY KEY, salesperson_id INTEGER,
    amount DECIMAL(10, 2), status TEXT
);
INSERT INTO deals VALUES
    (101, 1, 1000.00, 'Closed'),
    (102, 1, 500.00, 'Open'),
    (103, 2, 2000.00, 'Closed'),
    (104, 3, 1500.00, 'Closed');
