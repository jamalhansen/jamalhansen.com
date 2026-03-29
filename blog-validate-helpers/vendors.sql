CREATE TABLE IF NOT EXISTS vendors (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, headquarters_city TEXT
);
INSERT INTO vendors VALUES
    (1, 'Acme Supplies', 'Portland'),
    (2, 'Global Parts', 'Seattle'),
    (3, 'Quick Ship', NULL);
