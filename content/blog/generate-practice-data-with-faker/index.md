---
title: Generate Practice Data with faker
summary: Real SQL practice needs real-looking data. Generate hundreds of customers with Python's Faker library without downloading a single CSV
author:
  - Jamal Hansen
date: 2026-01-19
lastmod: 2026-01-13
tags:
  - "#python"
  - "#duckdb"
  - "#sql"
  - "#faker"
categories:
featureimage: jon-tyson-566CgCRSNCk-unsplash.jpg
cardimage: jon-tyson-566CgCRSNCk-unsplash-thumb.jpg
draft: false
toc: false
series: "SQL for Python Developers"
canonical_url: https://jamalhansen.com/blog/generate-practice-data-with-faker
slug: generate-practice-data-with-faker
layout: post

---

{{< unsplash-credit name="Jon Tyson" username="jontyson" photo-id="four-markers-on-table-566CgCRSNCk" >}}

Last week, we got DuckDB running with three hardcoded rows. That got us started—but three rows? You can eyeball that. Let's generate hundreds of realistic customers and build a dataset worth exploring.

Python has the perfect tool: `faker`. It's a library that generates realistic fake data—names, emails, addresses, dates—anything you'd find in a real database. Let's use it to build a dataset we can explore for the rest of this series.

## The Dataset: Customers

We'll create a customer table—the kind you'll find in almost any database:

```
customers
├── id (integer)
├── name (varchar)  
├── email (varchar)
├── city (varchar)
├── signup_date (date)
└── is_premium (boolean)
```

## Building Our Dataset

Now let's write the Python code that will:
- Generate 500 rows of data with `faker`
- Create the customer table
- Insert the generated data into the table
- Query that data to ensure it's there

To get started, we will install the `faker` module:
```bash
pip install faker
```

Now let's generate 500 customers:

```python
from faker import Faker
import random

fake = Faker()
Faker.seed(42)  # Same data every time
random.seed(42)

customers = []

for i in range(500):
    customers.append(
        {
            "id": i + 1,
            "name": fake.name(),
            "email": fake.email(),
            "city": fake.city(),
            "signup_date": fake.date_between(start_date="-2y", end_date="today"),
            "is_premium": random.choice([True, False, False, False]),
        }
    )

# Peek at what we generated
for c in customers[:3]:
    print(c)
```

```
{'id': 1, 'name': 'Allison Hill', 'email': 'davidjones@example.com', 'city': 'Joshuamouth', 'signup_date': datetime.date(2024, 8, 3), 'is_premium': False}
{'id': 2, 'name': 'Noah Rhodes', 'email': 'coleaustin@example.net', 'city': 'East Crystalbury', 'signup_date': datetime.date(2025, 6, 19), 'is_premium': False}
{'id': 3, 'name': 'David Ferguson', 'email': 'jenniferharris@example.org', 'city': 'Johnsonville', 'signup_date': datetime.date(2024, 5, 12), 'is_premium': False}
```

A few things to notice. First, `faker` can generate data for a variety of purposes and data types. We tell `faker` that we want a name or an email address, and it will generate not only a string, but an actual name or email address. 

It will also create randomized values such as dates within a range or a choice of values from a list. 

The `is_premium` line is a small trick: by putting `False` in the list three times, roughly 25% of customers end up as premium members. More realistic than a coin flip.

We are setting the random number seed at the beginning of the script. This makes the "random" data reproducible, so you'll get the same values every time you run it. This is useful in a number of situations, including testing. 

Now we have our generated data in the `customers` variable. Let's create a table for it to live in and then insert the data into the table. You'll notice `VARCHAR` in the CREATE TABLE statement—that's SQL's name for text data (like Python's `str`).

```python
import duckdb

con = duckdb.connect(':memory:')

con.execute("""
    CREATE TABLE customers (
        id INTEGER,
        name VARCHAR,
        email VARCHAR,
        city VARCHAR,
        signup_date DATE,
        is_premium BOOLEAN
    )
""")

con.executemany(
    "INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)",
    [
        (
            c['id'], 
            c['name'], 
            c['email'], 
            c['city'], 
            c['signup_date'], 
            c['is_premium']
        ) 
        for c in customers
    ]
)
```

Once the data has been inserted into the table, we can query it. Like last time, we just want to bring back all the records to see that they are there.

```python
# See the first few rows
result = con.execute("SELECT * FROM customers").fetchdf()
print(result.head(10))

# Or just specific columns
result = con.execute("SELECT name, city FROM customers").fetchdf()
print(result.head(10))
```

The `*` in `SELECT *` is shorthand for "all columns." Or you can list the columns that you want.

You should see ten unique customers—real-looking names, varied cities, a mix of premium and regular accounts. That's 500 rows of realistic data we can explore for the rest of this series.

## The Full Script

Here's everything in one runnable file:

```python
from faker import Faker
import random
import duckdb

# Generate fake data
fake = Faker()
Faker.seed(42)
random.seed(42)

customers = []
for i in range(500):
    customers.append(
        {
            "id": i + 1,
            "name": fake.name(),
            "email": fake.email(),
            "city": fake.city(),
            "signup_date": fake.date_between(start_date="-2y", end_date="today"),
            "is_premium": random.choice([True, False, False, False]),
        }
    )

# Load into DuckDB
con = duckdb.connect(':memory:')

con.execute("""
    CREATE TABLE customers (
        id INTEGER,
        name VARCHAR,
        email VARCHAR,
        city VARCHAR,
        signup_date DATE,
        is_premium BOOLEAN
    )
""")

con.executemany(
    "INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)",
    [
        (c['id'], c['name'], c['email'], c['city'], c['signup_date'], c['is_premium']) 
        for c in customers
    ]
)

# Query the data
result = con.execute("SELECT * FROM customers").fetchdf()
print(result.head(10))
```

## Try It Yourself

- **Scale it up**: Change `range(500)` to `range(10000)`. See how fast it handles larger data.
- **Change the seed**: Try `Faker.seed(123)`. Completely different people.
- **Bonus challenge**: Faker has `fake.user_name()`. Can you add a username column? You'll need to update the customer dict, the CREATE TABLE statement, and the INSERT query.

## Coming Up

We now have 500 customers to work with. In future posts, we'll filter them, sort them, and answer real questions about this data.

But there's one problem: every time you restart Python, this data disappears. Next week, we'll save the database to a file so you can keep building on it.
