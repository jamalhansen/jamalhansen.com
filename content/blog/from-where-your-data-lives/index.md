---
title: "FROM: Where Your Data Lives"
description: We write SELECT first, but FROM executes first. It's like the `for item in collection` part of a Python loop. You pick your data source before doing anything else.
author:
  - Jamal Hansen
date: 2026-02-09
tags:
  - sql
categories:
cover:
  image: "lance-chang-h3pVxOIpnzk-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Lance Chang"
    username: "carmendis"
    photo_id: "a-large-warehouse-filled-with-lots-of-shelves-h3pVxOIpnzk"
draft: false
ShowToc: false
series: "SQL for Python Developers"
layout: post
weight: 6
---

We have come a long way over the last five posts, but we are just getting started. So far, we have explored concepts that will help us along our journey, but haven't talked a whole lot about SQL itself. 

We have seen some basic SQL that uses a couple of keywords, `SELECT` and `FROM`, but we haven't looked very closely at what these do. Let's do that now, starting with `FROM`.

We start with `FROM` because it's the first thing the database *executes*, even though we write `SELECT` first. It tells the database where the data I am interested in comes from. Everything else (`SELECT`, `WHERE`, etc.) operates on what `FROM` gives you. Understanding execution order will save you debugging headaches later when we get to filtering and joins.

We have seen `FROM` in action with some basic SQL that looks like `SELECT name FROM customers;`

The way that the database reads this is `FROM customers` → then `SELECT name`

## Python Comparison

Let's go back to Python and work our way through the `for` loop, list comprehension, and SQL to explore further.

When writing a `for` loop, we tell Python where the data is, then what we want to do with it.

```python
for customer in customers:    # ← This is like FROM
    print(customer['name'])   # ← This is like SELECT
```

The list comprehension switches this up, putting what to do with the data first and then where it comes from second. This is more like SQL syntax. It is important to remember that just because the syntax order is reversed, the order that the logic executes remains the same. First find the source, then return what is wanted.
```python
# List comprehension - same order as SQL thinks
[c['name'] for c in customers]
# ↑ SELECT (second) ↑ FROM (first)   
```

SQL syntax is the same; the `FROM` identifies the source and then the desired data is returned.

```sql
SELECT name         -- ← This happens second
FROM customers      -- ← This happens first
```

## Examples

Using our practice database from [our previous post](https://jamalhansen.com/blog/dont-forget-to-save-persisting-your-duckdb-database), here are some examples of `FROM`. 

```sql
-- All columns from customers
SELECT * FROM customers

-- Specific columns from customers
SELECT name, email FROM customers

-- Just one column
SELECT city FROM customers
```

Try running these against your practice database to see them in action.

Later, we'll see queries that pull from other tables and even multiple tables at once. For now, we're working with our only table: `customers`.

## DuckDB Bonus: FROM Anywhere

DuckDB is a little different from a typical database engine and can read directly from files. Here is an example: 

```sql
-- FROM a CSV file
SELECT * FROM 'data/sales.csv'

-- FROM a Parquet file  
SELECT * FROM 'data/logs.parquet'
```

This is really cool functionality, but just a bonus that DuckDB gives us. Most databases don't allow this, and it is not standard SQL.

Now you know where your data comes from. Next week is `SELECT`, which chooses which columns you actually want to see.
