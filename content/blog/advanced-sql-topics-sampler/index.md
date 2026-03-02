---
title: Advanced SQL Topics Sampler
description: Quick tastes of CASE statements, JSON functions, date manipulation, set operations, and recursive CTEs. Enough to know what to learn next.
author:
  - Jamal Hansen
date: 2026-06-15
tags:
  - sql
categories:
cover:
  image: "lily-banse--YHSwy6uqvk-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Lily Banse"
    username: "lvnatikk"
    photo_id: "cooked-dish-on-gray-bowl--YHSwy6uqvk"
draft: false
ShowToc: false
series: "SQL for Python Developers"
unsplash_user: lvnatikk
---

You've spent 23 weeks building a SQL foundation. You can query, join, aggregate, test, and build pipelines. That covers most of what you'll do day to day.

But SQL has more to offer. This post is a sampler plate: six topics you'll encounter as your SQL work gets more complex. Some of these you'll use daily. Others you'll reach for once a quarter. All of them are worth knowing exist so you recognize them when the moment comes. We won't revisit COALESCE and NULLIF here since we covered those in [Post 15](https://jamalhansen.com/blog/null-the-value-that-isnt), but the six topics below are all new.

## CASE Statements for Conditional Logic

You'll reach for CASE statements constantly. They're SQL's if/else, and they show up any time you need to categorize, label, or calculate conditionally.

```sql
SELECT name,
       CASE 
           WHEN is_premium THEN 'VIP'
           WHEN signup_date > '2025-01-01' THEN 'New'
           ELSE 'Regular'
       END as customer_tier
FROM customers
```

In Python, the equivalent is a chained ternary expression:

```python
'VIP' if is_premium else ('New' if signup_date > '2025-01-01' else 'Regular')
```

CASE is more readable than that nested ternary, especially when you have four or five conditions. Use it to create categories, build custom sort orders, or handle conditional aggregation like `SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END)`.

## Date Functions

If you do any kind of reporting, date functions will become part of your daily vocabulary. They let you truncate timestamps to months or weeks, calculate intervals, and extract components like day-of-week for analysis.

```sql
SELECT 
    order_date,
    DATE_TRUNC('month', order_date) as month,
    order_date - INTERVAL '7 days' as week_ago,
    EXTRACT(dow FROM order_date) as day_of_week
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '30 days'
```

The Python equivalent uses `datetime` and `timedelta`:

```python
from datetime import datetime, timedelta

month = order_date.replace(day=1)
week_ago = order_date - timedelta(days=7)
day_of_week = order_date.weekday()
last_30_days = [o for o in orders if o['date'] >= datetime.now() - timedelta(days=30)]
```

SQL's `DATE_TRUNC` is particularly handy. Truncating to `'month'` or `'week'` gives you instant grouping buckets for time-series reporting without writing any rounding logic yourself.

## String Functions

String data in databases is rarely in the format you want. SQL provides manipulation functions that map closely to Python's string methods.

```sql
SELECT 
    UPPER(name) as upper_name,
    LOWER(email) as lower_email,
    SPLIT_PART(email, '@', 2) as email_domain,
    LENGTH(name) as name_length,
    TRIM(city) as clean_city
FROM customers
```

The Python equivalents are immediately recognizable:

```python
name.upper()
email.lower()
email.split('@')[1]
len(name)
city.strip()
```

You'll reach for these when cleaning messy data: trimming whitespace from imports, normalizing casing for comparisons, or extracting parts of structured strings like email domains or file paths.

## Set Operations

Sometimes you need to compare two result sets rather than join them. SQL's set operations work like Python's `set` type. Both result sets must have the same column structure.

- `UNION`: all unique rows from both sets (like `set_a | set_b`)
- `UNION ALL`: all rows from both sets, including duplicates (like `list_a + list_b`)
- `INTERSECT`: only rows in both sets (like `set_a & set_b`)
- `EXCEPT`: rows in the first set but not the second (like `set_a - set_b`)

```sql
-- All contacts from either source
SELECT email FROM customers
UNION
SELECT email FROM newsletter_subscribers

-- People who are both customers and subscribers
SELECT email FROM customers
INTERSECT
SELECT email FROM newsletter_subscribers

-- Customers who haven't subscribed to the newsletter
SELECT email FROM customers
EXCEPT
SELECT email FROM newsletter_subscribers
```

You won't use these every day, but they're the cleanest solution when you need to answer questions like "who's in list A but not list B?" or "combine these two data sources without duplicates."

## JSON Functions

DuckDB has strong JSON support, though the syntax varies across databases. You'll encounter JSON when working with API responses, event logs, or any semi-structured data stored in a text column.

```sql
SELECT 
    data->>'name' as name,
    data->'address'->>'city' as city
FROM events
WHERE data->>'type' = 'signup'
```

The Python equivalent is dictionary access:

```python
name = data['name']
city = data['address']['city']
```

The arrow operators are DuckDB's syntax for navigating JSON. Use `->` when you need to dig deeper into nested objects (it returns JSON, so you can chain it), and `->>` when you want the final value as a plain string for output or comparisons. PostgreSQL uses the same operators. MySQL and SQLite have different approaches (`JSON_EXTRACT`), so check your database's documentation when you need this.

## Recursive CTEs

We covered CTEs back in [Post 14](https://jamalhansen.com/blog/ctes-making-your-sql-readable). Recursive CTEs take that concept further: they reference themselves, building results iteratively until a stopping condition is met.

Two situations where I reach for these: generating a series of dates for time-based reporting (when you need every day in a range, even days with no data), and traversing hierarchical data like organizational charts or category trees.

```sql
WITH RECURSIVE dates AS (
    SELECT DATE '2025-01-01' as date
    UNION ALL
    SELECT date + INTERVAL '1 day'
    FROM dates
    WHERE date < '2025-01-31'
)
SELECT * FROM dates
```

In Python, the closest equivalent is a while loop that appends to a list until a condition is met:

```python
from datetime import date, timedelta

dates = []
current = date(2025, 1, 1)
while current <= date(2025, 1, 31):
    dates.append(current)
    current += timedelta(days=1)
```

A word of caution: always include a clear stopping condition in the WHERE clause. A recursive CTE without one will run until your database kills it or runs out of memory.

## Exercises

### Exercise 1: CASE Statement Tiers

Using the customers and orders tables, write a query that categorizes customers into spending tiers based on their total order amount: 'High' (over $500), 'Medium' ($100-$500), and 'Low' (under $100). Include customers with no orders as 'No Orders'.

Hint: you'll need a LEFT JOIN and COALESCE from [Post 15](https://jamalhansen.com/blog/null-the-value-that-isnt).

### Exercise 2: Monthly Revenue Report

Using the orders table, write a query that shows total revenue by month using DATE_TRUNC. Include only the last 6 months and order the results chronologically.

### Exercise 3: String Cleanup

Write a query that finds all customers whose email domain (everything after the @) is 'gmail.com'. Write it two ways: once using SPLIT_PART and once using LIKE. Compare which reads more clearly to you.

### Exercise 4: Set Operations

Assume you have a `customers` table and a `newsletter_subscribers` table, both with an `email` column. Write three queries:

- Subscribers who aren't customers
- Customers who aren't subscribers
- People who are both

### Exercise 5: Generate a Date Series

Write a recursive CTE that generates every Monday in 2025. Then LEFT JOIN it against an orders table grouped by week to find weeks with zero orders.

Hint: the LEFT JOIN + NULL pattern from [Post 12](https://jamalhansen.com/blog/joins-explained-for-python-developers) is exactly what you need here.

## What's Next

You've built a complete SQL foundation. Next week: we celebrate your journey, review what you've learned, and point you toward what comes after.