---
slug: testing-sql-code
title: Testing SQL Code
description: Test queries like Python code using in-memory databases, fixtures, and pytest. Fresh data per test, no state leakage.
author:
  - Jamal Hansen
date: 2026-06-08
tags:
  - sql
categories:
cover:
  image: "jakub-zerdzicki-dEe2r9CmoAo-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Jakub Żerdzicki"
    username: "jakubzerdzicki"
    photo_id: "someone-is-writing-on-a-tablet-with-a-stylus-dEe2r9CmoAo"
draft: false
ShowToc: false
series: "SQL for Python Developers"
unsplash_user: jakubzerdzicki
---
<!-- test:needs: customers, orders -->
You test your Python code. You probably don't test your SQL. Here's why you should, and how to start.

I once had a query that ran fine for months. Then someone added a column to the source table and a `SELECT *` downstream started returning unexpected data. The query didn't error. It just silently gave wrong results. A test would have caught it immediately.

Schema changes break queries silently. Refactoring a CTE can shift results in ways you don't notice. New data patterns expose assumptions you didn't know you made. SQL deserves the same testing discipline as the rest of your code, and Python makes it straightforward.

## The Challenge

When we try to write tests for SQL, one issue that we run into right away is that, unlike Python, when we try to Arrange, Act, Assert, there is no function to Act upon.

In Python, you might have the following function.
```python
def add(a, b):
    return a + b
```

Writing a test for this is straightforward:

```python
def test_add():
    actual = add(2, 5)
    assert actual == 7
```

If we try something like this with SQL, we run into an issue because the SQL is dependent upon a database and data. We need a way to supply both the database and the data as part of the test itself.

## Strategy: In-Memory Test Database

Standing up a clean new database as a fixture for each test seems like a lot of overhead, but DuckDB's in-memory databases make it snappy. 
```python
import pytest
import duckdb

@pytest.fixture
def test_db():
    """Create fresh in-memory database for each test."""
    con = duckdb.connect(':memory:')
    
    # Create tables
    con.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name VARCHAR,
            city VARCHAR,
            is_premium BOOLEAN
        )
    """)
    
    # Seed test data
    con.execute("""
        INSERT INTO customers VALUES
        (1, 'Alice', 'New York', true),
        (2, 'Bob', 'New York', false),
        (3, 'Carol', 'Denver', true),
        (4, 'Dave', 'Denver', false)
    """)
    
    return con
```

If you've used Python's `unittest.setUp()`, this is the same idea. Each test gets a fresh database with known data, so tests never interfere with each other.

## Test a Simple Query

Now let's test a simple query using this fixture.
```python
def test_count_premium_customers(test_db):
    result = test_db.execute("""
        SELECT COUNT(*) FROM customers WHERE is_premium = true
    """).fetchone()[0]
    
    assert result == 2  # Alice and Carol

def test_customers_by_city(test_db):
    result = test_db.execute("""
        SELECT city, COUNT(*) as count
        FROM customers
        GROUP BY city
        ORDER BY city
    """).fetchall()
    
    assert result == [('Denver', 2), ('New York', 2)]
```

We created the data, so we know the results to expect and can assert the expected result. 

Save these in a file called `test_queries.py` and run them with pytest:

```bash
pytest test_queries.py -v
```

You should see output like this:

```
test_queries.py::test_count_premium_customers PASSED
test_queries.py::test_customers_by_city PASSED

================ 2 passed in 0.08s ================
```

Green across the board. Each test spun up its own database, ran the query, and checked the result in under a tenth of a second.

## Test Query Functions

Let's look at a slightly more complex situation. We have a function that we want to test, and that function issues SQL against a database. 

Here we have a function `get_premium_customers()` which accepts a database connection and an optional city value. The function returns all premium customers for that city (if specified).

```python
# The function we're testing
def get_premium_customers(con, city=None):
    query = "SELECT name FROM customers WHERE is_premium = true"
    params = {}
    if city:
        query += " AND city = $city"
        params["city"] = city
    return con.execute(query, params).fetchall()

# Test
def test_get_premium_customers_all(test_db):
    result = get_premium_customers(test_db)
    names = [r[0] for r in result]
    assert set(names) == {"Alice", "Carol"}

def test_get_premium_customers_by_city(test_db):
    result = get_premium_customers(test_db, city="Denver")
    names = [r[0] for r in result]
    assert names == ["Carol"]
```

We can simply write tests to check that it works when we do and when we don't specify a city. This is the pattern you'll use most in practice: testing Python functions that build and execute SQL.

## Testing Edge Cases

Using the fixture, we can also test for edge cases such as querying for non-existent cities or inserting `NULL`s to ensure that they are handled as expected. 

```python
def test_empty_results(test_db):
    result = test_db.execute("""
        SELECT * FROM customers WHERE city = 'Nonexistent'
    """).fetchall()
    
    assert result == []

def test_null_handling(test_db):
    test_db.execute("INSERT INTO customers VALUES (5, 'Eve', NULL, false)")
    
    result = test_db.execute("""
        SELECT COUNT(*) FROM customers WHERE city IS NULL
    """).fetchone()[0]
    
    assert result == 1
```

## Fixtures for Complex Schemas

Real queries span multiple tables. Your fixtures should too.

```python
@pytest.fixture
def test_db_with_orders():
    """Database with customers and orders."""
    con = duckdb.connect(':memory:')
    
    con.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, name VARCHAR)")
    con.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            amount DECIMAL(10,2)
        )
    """)
    
    con.execute("INSERT INTO customers VALUES (1, 'Alice'), (2, 'Bob')")
    con.execute("""
        INSERT INTO orders VALUES 
            (1, 1, 100.00),
            (2, 1, 200.00),
            (3, 2, 50.00)
    """)
    
    return con

def test_customer_totals(test_db_with_orders):
    result = test_db_with_orders.execute("""
        SELECT c.name, SUM(o.amount) as total
        FROM customers c
        JOIN orders o ON c.id = o.customer_id
        GROUP BY c.id, c.name
        ORDER BY total DESC
    """).fetchall()
    
    assert result[0] == ('Alice', 300.00)
    assert result[1] == ('Bob', 50.00)
```

I've used separate `execute()` calls for each statement here. DuckDB can handle multiple statements in a single call, but SQLite and PostgreSQL can't, so splitting them is a good habit for portable code.

With a little help from Python and pytest, testing SQL is not that hard. It just takes standing up some fixtures. You can now write SQL, optimize it, secure it with [parameterized queries](https://jamalhansen.com/blog/parameterized-queries-and-security), and test it. That's a complete professional toolkit.

## Exercises

### Exercise 1: Test a WHERE Clause

Using the `test_db` fixture from earlier in this post, write tests that verify the following queries return the correct results:

- All customers from Denver
- All non-premium customers
- Customers whose name starts with 'A'

Each test should assert both the number of rows returned and the actual values.

### Exercise 2: Test a LEFT JOIN

Using the `test_db_with_orders` fixture, write a test that verifies a LEFT JOIN correctly identifies customers with no orders. You'll need to either modify the fixture to include a third customer with no orders, or insert one within the test itself. Then assert that your query finds them.

Hint: Remember the LEFT JOIN + IS NULL pattern from [Post 12](https://jamalhansen.com/blog/joins-explained-for-python-developers).

### Exercise 3: Test Edge Cases

Create a new fixture called `test_db_edge_cases` with data that includes NULL values, empty strings, and duplicate cities. Then write tests for:

- `COUNT(*)` vs `COUNT(column)` returns different numbers when NULLs are present
- `GROUP BY` groups NULL values into a single bucket
- An empty result set returns an empty list, not an error

### Exercise 4: Test a CTE Pipeline

Write a test for this CTE query using the `test_db_with_orders` fixture. You know the input data, so calculate the expected output by hand first, then assert against it.

```sql
WITH customer_totals AS (
    SELECT customer_id, SUM(amount) as total_spent
    FROM orders
    GROUP BY customer_id
),
above_average AS (
    SELECT customer_id, total_spent
    FROM customer_totals
    WHERE total_spent > (SELECT AVG(total_spent) FROM customer_totals)
)
SELECT c.name, a.total_spent
FROM above_average a
JOIN customers c ON a.customer_id = c.id
```

### Exercise 5: Test for Failure

Not all tests check for correct results. Sometimes you want to verify that bad operations fail properly. Using pytest's `pytest.raises`, write a test that:

- Attempts to insert a duplicate primary key and asserts that it raises an error
- Attempts to insert a row with a NULL value into a NOT NULL column and asserts that it fails

Hint: You may need to add constraints to the fixture's CREATE TABLE statement.

```python
def test_duplicate_primary_key(test_db):
    with pytest.raises(Exception):
        test_db.execute("INSERT INTO customers VALUES (1, 'Duplicate', 'NYC', true)")
```

## What's Next

You've learned SQL from basics to testing. Next, we'll look at a sampler of advanced topics: CASE statements, JSON, dates, and set operations.