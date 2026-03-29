---
title: Parameterized Queries & Security
description: String formatting in SQL is dangerous. Learn parameterized queries to keep user input safe and prevent SQL injection attacks.
author:
  - Jamal Hansen
date: 2026-05-25
tags:
  - sql
cover:
  image: "eyasu-etsub-_enXmoXudAk-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Eyasu Etsub"
    username: "jphotography2012"
    photo_id: "a-broken-glass-window-with-a-field-in-the-background-_enXmoXudAk"
draft: false
ShowToc: false
series: "SQL for Python Developers"
unsplash_user: jphotography2012
---
<!-- test:needs: customers -->

As a Python developer, you are aware of software vulnerabilities. You have probably heard of SQL injection attacks, and you may have even done some work to protect against them.

Today, we are going to discuss what they are and how easy it is to prevent them.

## SQL Injection

So let's say your application has a customer search screen. That screen allows users to search for customers by city. The user enters the city they are interested in, and you take the city they entered and make some SQL to search for customers in that city.

<!-- test:skip -->
```python
# NEVER DO THIS!!
user_input = input("Enter city: ")
query = f"SELECT * FROM customers WHERE city = '{user_input}'"
con.execute(query)
```

.. and you just exposed yourself to a SQL injection attack! This vulnerability allows an attacker to issue whatever commands they want to your database, gathering your data or dropping your tables. How?

What if user enters: `'; DROP TABLE customers; --`

The query becomes:
```sql
SELECT * FROM customers WHERE city = ''; DROP TABLE customers; --'
```

The semicolon ends the first command, and a second one runs: one that drops your customers table. This is clearly not what we want to allow.

## Python Comparison

When we take user input and append it to a SQL statement, we are effectively taking their input and executing it. In Python that would look something like this.

<!-- test:skip -->
```python
code = f"print({user_input})"
exec(code)  # Arbitrary code execution!
```

We wouldn't want to allow that.

## The Solution: Parameterized Queries

Thankfully, SQL (and database clients) have made a simple way to avoid SQL Injection attacks: parameterized queries.

With parameterized queries, you keep the user input separate from the SQL and the client will safely pass the values to the database so that they will be used as intended to filter the results.

Here is an example of a parameterized query.
<!-- test:skip -->
```python
city = input("Enter city: ")
con.execute("SELECT * FROM customers WHERE city = ?", [city])
```

Notice that the `execute()` Python command takes two parameters. The first is the SQL, except that the SQL has a `?` where the user's value should be. The second is a list containing the user-supplied value. This will safely execute the desired SQL.

Alternatively, you could name the parameters if you prefer. This is easier to read if you start having many parameters in your SQL.
<!-- test:skip -->
```python
con.execute("SELECT * FROM customers WHERE city = $city", {"city": city})
```

Using parameterized queries, the database treats parameters as *data*, and never as *code*.

You may also hear the term "prepared statements." These are a related concept where the database pre-compiles the query plan. In DuckDB, parameterized queries give you the safety benefits without needing to worry about the distinction.

## Practical Examples

In addition to searching for results, here are some more examples of how your application might use parameterized queries.

You have a new customer. Yay! Before they can order, you need to add the new customer to the database. All of this customer's data is supplied by a user and cannot be trusted.

No need to worry, parameterized queries can help.
```python
def add_customer(name, email, city):
    con.execute(
        "INSERT INTO customers (name, email, city) VALUES (?, ?, ?)",
        [name, email, city]
    )
```

Notice that there are multiple `?`s in the SQL and that there are also multiple values supplied in the parameter list? These will be substituted in order.

There is also an `executemany()` available in the DuckDB client if you need to insert multiple customer records at once.

<!-- test:skip -->
```python
customers = [
    ("Alice", "alice@example.com", "Denver"),
    ("Bob", "bob@example.com", "Austin"),
]
con.executemany(
    "INSERT INTO customers (name, email, city) VALUES (?, ?, ?)",
    customers
)
```

In real applications, you often need to build queries dynamically based on which filters a user has selected. Named parameters make this clean and readable.

```python
def search_customers(city=None, is_premium=None):
    query = "SELECT * FROM customers WHERE 1=1"
    params = {}
    
    if city is not None:
        query += " AND city = $city"
        params["city"] = city
    
    if is_premium is not None:
        query += " AND is_premium = $premium"
        params["premium"] = is_premium
    
    return con.execute(query, params).fetchdf()
```

The `WHERE 1=1` is a handy trick. It gives you a base condition that is always true, so every additional filter can simply start with `AND` without needing to special-case the first one.

## What Parameters Can't Do

Parameters are for *values*, not structure. You cannot parameterize table names or column names.

<!-- test:skip -->
```python
# This WON'T work
con.execute("SELECT * FROM ?", [table_name])

# This also WON'T work
con.execute("SELECT ? FROM customers", [column_name])
```

If you need dynamic table or column names, validate against a whitelist instead.

<!-- test:skip -->
```python
ALLOWED_TABLES = {"customers", "orders", "products"}
if table_name in ALLOWED_TABLES:
    con.execute(f"SELECT * FROM {table_name}")
```

This is safe because you are controlling which values are allowed, not the user.

## Exercises

### Exercise 1: Fix the Vulnerability

The following code has a SQL injection vulnerability. Rewrite it using parameterized queries.

<!-- test:skip -->
```python
import duckdb

con = duckdb.connect("shop.db")

product_name = input("Search for product: ")
min_price = input("Minimum price: ")

query = f"SELECT * FROM products WHERE name LIKE '%{product_name}%' AND price >= {min_price}"
results = con.execute(query).fetchall()

for row in results:
    print(row)
```

**Hint:** Remember that `LIKE` patterns work fine as parameter values. You can build the pattern string in Python and pass it as a parameter.

<details>
<summary>Solution</summary>

<!-- test:skip -->
```python
import duckdb

con = duckdb.connect("shop.db")

product_name = input("Search for product: ")
min_price = input("Minimum price: ")

# Build the LIKE pattern in Python, pass it safely as a parameter
search_pattern = f"%{product_name}%"

results = con.execute(
    "SELECT * FROM products WHERE name LIKE ? AND price >= ?",
    [search_pattern, float(min_price)]
).fetchall()

for row in results:
    print(row)
```

The key insight: the `%` wildcards are part of the *value*, not the SQL structure, so they go into the parameter. The database handles them safely.

</details>

### Exercise 2: Build a Dynamic Filter with Named Parameters

Write a function called `search_orders()` that accepts three optional keyword arguments: `customer_name`, `status`, and `min_total`. The function should build a parameterized query that only filters on the arguments that are provided (not `None`). Use named parameters (`$param` syntax).

Example usage:
<!-- test:skip -->
```python
# All orders over $100
search_orders(min_total=100)

# Pending orders for Alice
search_orders(customer_name="Alice", status="pending")

# All orders (no filters)
search_orders()
```

<details>
<summary>Solution</summary>

```python
def search_orders(customer_name=None, status=None, min_total=None):
    query = "SELECT * FROM orders WHERE 1=1"
    params = {}

    if customer_name is not None:
        query += " AND customer_name = $customer_name"
        params["customer_name"] = customer_name

    if status is not None:
        query += " AND status = $status"
        params["status"] = status

    if min_total is not None:
        query += " AND total >= $min_total"
        params["min_total"] = min_total

    return con.execute(query, params).fetchdf()
```

This uses the `WHERE 1=1` pattern we covered earlier in the post to make appending filters clean and consistent.

</details>

### Exercise 3: Safe Bulk Insert with Validation

You receive a list of new product records from an external source. Write code that:
1. Validates each record has all required fields (name, price, category)
2. Rejects any records where price is not a positive number
3. Inserts all valid records using `executemany()`
4. Prints how many records were inserted and how many were rejected

```python
incoming_products = [
    {"name": "Widget", "price": 9.99, "category": "Tools"},
    {"name": "Gadget", "price": -5.00, "category": "Electronics"},  # bad price
    {"name": "Doohickey", "price": 3.50, "category": "Tools"},
    {"name": "Thingamajig", "category": "Misc"},  # missing price
    {"name": "Sprocket", "price": 12.00, "category": "Hardware"},
]
```

<details>
<summary>Solution</summary>

<!-- test:skip -->
```python
valid_records = []
rejected_count = 0

required_fields = {"name", "price", "category"}

for product in incoming_products:
    # Check all required fields exist
    if not required_fields.issubset(product.keys()):
        rejected_count += 1
        continue

    # Check price is a positive number
    if not isinstance(product["price"], (int, float)) or not (product["price"] > 0):
        rejected_count += 1
        continue

    valid_records.append((product["name"], product["price"], product["category"]))

if valid_records:
    con.executemany(
        "INSERT INTO products (name, price, category) VALUES (?, ?, ?)",
        valid_records
    )

print(f"Inserted: {len(valid_records)}")
print(f"Rejected: {rejected_count}")
# Output: Inserted: 3, Rejected: 2
```

This combines validation (a Python strength) with safe bulk insertion (parameterized `executemany()`). In real ETL work, you would also want to log *why* each record was rejected.

</details>

## Next Week

You now know how to write safe SQL. But what about Object Relational Mappers (ORMs)? These are helpful libraries that translate objects to SQL and back. Next week, we'll look at when an ORM makes sense and when raw SQL is the better tool.
