CREATE TABLE IF NOT EXISTS events (data JSON);
INSERT INTO events VALUES
    ('{"type": "signup", "name": "John Doe", "address": {"city": "New York"}}'),
    ('{"type": "login", "name": "John Doe"}'),
    ('{"type": "signup", "name": "Jane Smith", "address": {"city": "Los Angeles"}}');
