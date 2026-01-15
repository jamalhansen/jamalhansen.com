---
title: Don't forget to save! Persisting your DuckDB database
summary: Your in-memory database disappears when Python exits. Let's fix that with a one-line change that saves everything to disk.
author:
  - Jamal Hansen
date: 2026-01-26
lastmod: 2026-01-14
tags:
  - duckdb
  - sql
categories:
featureimage: s-j-yJVpnfqu8GY-unsplash.jpg
cardimage: s-j-yJVpnfqu8GY-unsplash-thumb.jpg
draft: false
toc: false
series: "SQL for Python Developers"
canonical_url: https://jamalhansen.com/blog/dont-forget-to-save-persisting-your-duckdb-database
slug: dont-forget-to-save-persisting-your-duckdb-database
layout: post

---
{{< unsplash-credit name="s j" username="sjjillan" photo-id="a-group-of-electronic-devices-yJVpnfqu8GY" >}}

I still remember losing schoolwork and video game progress because I forgot to save. That sinking feeling when hours of work vanish because you were too caught up in the flow to pause and save.

[In our last post](/blog/your-first-sql-table-its-just-a-dataframe-with-rules), we created a customer database and generated 500 rows of fake data. Our in-memory database has the same problem—when Python exits, all that data vanishes:

```python
import duckdb

con = duckdb.connect(':memory:')
con.execute("CREATE TABLE customers (id INT, name VARCHAR)")
con.execute("INSERT INTO customers VALUES (1, 'Alice')")
print(con.execute("SELECT * FROM customers").fetchdf())
# Script ends... and the data is gone forever
```

A database is supposed to provide persistent storage, isn't it? Let's fix that with one small change.

## The One-Line Fix

So far, we've been creating our connection like this:
```python
import duckdb
con = duckdb.connect(':memory:')
```

If we connect using a file path rather than the `:memory:` keyword, DuckDB stores everything to that file:

```python
import duckdb
con = duckdb.connect('practice.duckdb')
```

That's it. One small change.

## Persistent Data Storage

Now, let's upgrade our customer generation script to use persistent storage. This version uses a handy `CREATE TABLE IF NOT EXISTS`, which will only create the table when it isn't there. This avoids errors that happen when you run the script multiple times. 

```python
from faker import Faker
import duckdb
import random

# Connect to a FILE instead of memory
con = duckdb.connect('practice.duckdb')

# CREATE TABLE IF NOT EXISTS lets us run this script repeatedly
con.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER,
        name VARCHAR,
        email VARCHAR,
        city VARCHAR,
        signup_date DATE,
        is_premium BOOLEAN
    )
""")

# Only generate data if the table is empty
row_count = con.execute("SELECT COUNT(*) FROM customers").fetchone()[0]

if row_count == 0:
    fake = Faker()
    Faker.seed(42)
    random.seed(42)
    
    customers = []
    for i in range(500):
        customers.append((
            i + 1,
            fake.name(),
            fake.email(),
            fake.city(),
            fake.date_between(start_date='-2y', end_date='today'),
            random.choice([True, False, False, False])
        ))
    
    con.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)",
        customers
    )
    print("Created 500 customers!")
else:
    print(f"Data already exists! ({row_count} customers)")

# Either way, we can query it
print(con.execute("SELECT * FROM customers").fetchdf().head())
```

## Proving It Persists

In a fresh Python session:

```python
import duckdb

# The file persists between Python sessions
con = duckdb.connect('practice.duckdb')

# Data is still there!
print(con.execute("SELECT * FROM customers").fetchdf().head())
```

The data survived. Now you have a persistent database with 500 customers ready for querying.

## What's Next

So far, we've only written SQL that brings back all the data in a table. To move forward quickly, we need to make a mental model for how SQL works. SQL is more like a list comprehension than a `for` loop, and next week we'll explore this mental shift.
