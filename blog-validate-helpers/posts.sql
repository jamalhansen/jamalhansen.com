CREATE TABLE IF NOT EXISTS posts (
    id INTEGER, userId INTEGER, title VARCHAR, body VARCHAR
);
INSERT INTO posts VALUES
    (1, 1, 'sample post title alpha', 'body alpha'),
    (2, 1, 'sample post title beta', 'body beta'),
    (3, 2, 'sample post title gamma', 'body gamma'),
    (4, 2, 'sample post title delta', 'body delta'),
    (5, 3, 'sample post title epsilon', 'body epsilon');
