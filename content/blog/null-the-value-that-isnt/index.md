---
title: "NULL: The Value That Isn't"
description: NULL means "unknown," not "empty." Why NULL = NULL isn't true, three-valued logic, and how NULL behaves in WHERE, GROUP BY, JOINs, and subqueries. Master COALESCE and NULLIF.
author:
  - Jamal Hansen
date: 2026-04-13
tags:
  - sql
categories:
cover:
  image: "james-lee-lnIwKspeuTs-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "James Lee"
    username: "picsbyjameslee"
    photo_id: "stars-in-the-sky-during-night-time-lnIwKspeuTs"
draft: false
ShowToc: false
series: "SQL for Python Developers"
weight: 15
---
This post is about nothing, or rather, it's about the unknown. By now, you've bumped into `NULL` several times. Let's finally make sense of it.

The SQL `NULL` is sort of like `None` in Python. After all, they both represent the lack of a value, right?

```python
value = None
if value == None:  # True (though `is None` is preferred)
    print("It's None")

print(None == None)  # True
```

In Python, `None` is a thing you can compare. Let's see how `NULL` compares.

```sql
SELECT * FROM customers WHERE middle_name = NULL;  -- Returns NOTHING
SELECT * FROM customers WHERE middle_name IS NULL;  -- Correct!
```

In SQL, `NULL` means "I don't know," and you can't know if two unknowns are equal.

`NULL` is not a value. It means "unknown" or "missing." Once you start thinking of it this way, `NULL` behavior becomes predictable instead of frustrating.

## Setup: Expanding Our Customers Table

Our customers table has served us well, but to really explore NULL behavior we need columns where missing data is natural. Not every customer provides a phone number. Not everyone has a middle name. Let's add a few columns to our table using `ALTER TABLE` and then populate them with Faker.

```sql
ALTER TABLE customers ADD COLUMN middle_name VARCHAR;
ALTER TABLE customers ADD COLUMN nickname VARCHAR;
ALTER TABLE customers ADD COLUMN phone VARCHAR;
ALTER TABLE customers ADD COLUMN state VARCHAR;
ALTER TABLE customers ADD COLUMN status VARCHAR;
```

Now let's populate them with realistic data. Some values will be NULL on purpose, because that's how real data works.

```python
from faker import Faker
import random
import duckdb

fake = Faker()
Faker.seed(42)
random.seed(42)

con = duckdb.connect('practice.duckdb')

for row in con.execute("SELECT id FROM customers").fetchall():
    customer_id = row[0]

    middle_name = fake.first_name() if random.random() < 0.6 else (
        "" if random.random() < 0.15 else None
    )
    nickname = fake.first_name() if random.random() < 0.2 else None
    phone = fake.phone_number() if random.random() < 0.7 else None
    state = fake.state() if random.random() < 0.85 else None
    status = random.choice(
        ['active', 'active', 'active', 'inactive', 'unknown', None]
    )

    con.execute("""
        UPDATE customers 
        SET middle_name = ?, nickname = ?, phone = ?, state = ?, status = ?
        WHERE id = ?
    """, [middle_name, nickname, phone, state, status, customer_id])
```

A few things to notice about the data we're generating. About 60% of customers get a middle name, but some get an empty string instead of NULL. That's a common data quality issue you'll run into in real databases, and we'll use it in one of the challenges later. Only 20% have a nickname. About 30% are missing a phone number, and 15% have no state on file. The status column has a mix of 'active', 'inactive', 'unknown', and NULL values.

Run a quick check to see the new columns:

```sql
SELECT name, middle_name, nickname, phone, state, status
FROM customers
LIMIT 10;
```

You should see a mix of values and NULLs. That's exactly what we want.

## Three-Valued Logic

Most programming languages have two truth values: true and false. SQL has three: TRUE, FALSE, and NULL.

Think of NULL as "I don't know." When you combine something with "I don't know," the result depends on whether the unknown matters.

| Expression      | Result | Why                                              |
| --------------- | ------ | ------------------------------------------------ |
| TRUE AND NULL   | NULL   | Could be TRUE AND TRUE or TRUE AND FALSE. Unknown. |
| FALSE AND NULL  | FALSE  | Doesn't matter what the NULL is. Still FALSE.      |
| TRUE OR NULL    | TRUE   | Doesn't matter what the NULL is. Still TRUE.       |
| FALSE OR NULL   | NULL   | Could be FALSE OR TRUE or FALSE OR FALSE. Unknown. |
| NOT NULL        | NULL   | The opposite of unknown is still unknown.          |

Imagine if `None` in Python were contagious: any operation involving it returned `None` instead of raising an error. That's essentially what SQL does with NULL.

This matters because WHERE clauses only return rows where the condition is TRUE. If a comparison involves NULL and the result is NULL (not TRUE), that row gets filtered out. This is the root of almost every NULL surprise.

## NULL Behavior You've Already Seen

You've already encountered NULL in previous posts. Let's connect the dots.

### WHERE

In a [WHERE clause](https://jamalhansen.com/blog/where-filtering-your-data), adding an equals condition to a column quietly excludes `NULL` values from your results. Both of the following will exclude `NULL` values in the status column.

```sql
SELECT * FROM customers WHERE status = 'active';     -- Excludes NULL
SELECT * FROM customers WHERE status != 'active';    -- ALSO excludes NULL!
```

That second one catches people. If status is NULL, then `NULL != 'active'` evaluates to NULL, not TRUE, so the row doesn't make the cut. To include NULL values, you have to ask for them explicitly.

```sql
SELECT * FROM customers WHERE status != 'active' OR status IS NULL;  
```

### GROUP BY and Aggregation

When grouping with the [GROUP BY clause](https://jamalhansen.com/blog/group-by-aggregating-your-data), all NULL values group together into one bucket. This is actually useful for reporting on "unknown" categories.

```sql
SELECT state, COUNT(*) FROM customers GROUP BY state;
-- NULLs form their own group: (NULL, 15)
```

Another place to watch for NULLs is the `COUNT()` function. `COUNT(*)` counts all rows, including those with NULL values. But if you pass a column to `COUNT()`, it only counts the non-NULL values. Because of this, I don't pass a column to `COUNT()` unless I specifically want to exclude NULLs.

```sql
SELECT 
    COUNT(*) as total_rows,           -- 500
    COUNT(middle_name) as has_middle  -- ~340 (rest are NULL)
FROM customers;
```

### JOINs

We already know that NULL won't work with equals, so it shouldn't be a surprise that NULL values won't match in a [JOIN](https://jamalhansen.com/blog/joins-explained-for-python-developers) condition either. NULL = NULL is NULL, not TRUE, so no match.

However, when you use a `LEFT JOIN`, the columns from the right table come back as NULL for rows that don't have a match. This is often where unexpected NULLs sneak into your results.

```sql
SELECT c.name, o.order_date
FROM 
	customers c LEFT JOIN 
	orders o ON c.id = o.customer_id;
```

### Subqueries with NOT IN

This one is nasty. Remember [subqueries](https://jamalhansen.com/blog/subqueries-when-sql-needs-helper-functions) from two weeks ago? If you use `NOT IN` with a subquery that returns any NULL values, you might get zero rows back.

To show this, let's add a small `vendors` table to our sample database. Some vendors have a headquarters city, but not all of them.

```sql
CREATE TABLE vendors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    headquarters_city TEXT
);

INSERT INTO vendors (name, headquarters_city) VALUES
    ('Acme Supplies', 'Portland'),
    ('Global Parts', 'Seattle'),
    ('Quick Ship', NULL);
```

Now watch what happens when we try to find customers whose city doesn't match any vendor headquarters.

```sql
SELECT * 
FROM customers
WHERE city NOT IN (
	SELECT headquarters_city 
	FROM vendors
	);
```

If `headquarters_city` is NULL for even one vendor, this entire query returns nothing. Why? Because `city NOT IN ('Portland', 'Seattle', NULL)` asks "is city not equal to 'Portland' AND not equal to 'Seattle' AND not equal to NULL?" That last comparison evaluates to NULL, which makes the whole AND chain NULL, which means no rows pass the filter.

The fix is to either filter NULLs out of your subquery or use `NOT EXISTS` instead.

```sql
-- Option 1: Filter NULLs from the subquery
SELECT * FROM customers
WHERE city NOT IN (
    SELECT headquarters_city FROM vendors WHERE headquarters_city IS NOT NULL
);

-- Option 2: Use NOT EXISTS
SELECT * FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM vendors v WHERE v.headquarters_city = c.city
);
```

## Your NULL Toolkit

Working with NULL can be confusing, especially at first. Here are the tools that keep things manageable.

### IS NULL / IS NOT NULL

Always use `IS NULL` or `IS NOT NULL` when checking for null values. The equals operator will not work.

```sql
SELECT * FROM customers WHERE phone IS NULL;
SELECT * FROM customers WHERE phone IS NOT NULL;
```

### COALESCE

The `COALESCE()` function takes as many values as you want and returns the first one that is not NULL, working left to right.

This will return '(Not Found)' rather than `NULL` if middle_name is null.

```sql
SELECT COALESCE(middle_name, '(Not Found)') as middle_name FROM customers;
```

This SQL will return the nickname if present, otherwise the customer's name. If neither is available, 'Unknown' is returned.

```sql
SELECT COALESCE(nickname, name, 'Unknown') as display_name FROM customers;
```

In Python terms, `COALESCE` is like `value if value is not None else default`, but it can chain through multiple fallbacks.

### NULLIF

`NULLIF()` is the reverse of `COALESCE`. It takes two values and returns NULL if they're equal, otherwise it returns the first value. The following will return status as `NULL` if the value in the status column is 'unknown'.

```sql
SELECT NULLIF(status, 'unknown') as status FROM customers;
```

Where this really shines is in preventing division by zero errors.

```sql
SELECT total / NULLIF(count, 0) as average FROM stats;
```

Without `NULLIF`, dividing by zero throws an error. With it, you get a NULL that you can handle with `COALESCE` if you need a default value. They work well together.

```sql
SELECT COALESCE(total / NULLIF(count, 0), 0) as average FROM stats;
-- Returns 0 instead of NULL when count is 0
```

## Try It Yourself

These use our customers and orders sample database.

### Challenge 1: Find the Gaps

Write a query that returns customers who are missing a middle name (`NULL`) or have an empty string as a middle name. These are two different conditions. 

### Challenge 2: Two Ways to Find Customers Without Orders

We solved this with a LEFT JOIN in Post 12 and with NOT IN in Post 13. Now write it both ways, making sure your NOT IN version handles NULLs safely.

First, you will use an outer join to find the rows by adding a `WHERE` clause to the following statement.

```sql
SELECT c.name
FROM 
	customers c LEFT JOIN 
	orders o ON c.id = o.customer_id
```

Next, make this NOT IN version NULL-safe.

```sql
-- Way 2: NOT IN (NULL-safe)
SELECT name FROM customers
WHERE id NOT IN (
    SELECT customer_id FROM orders
)
```

### Challenge 3: NULL-Safe Customer Report

Write a query that returns all customers with these columns:
- name
- middle name
- city
- total order count (default to 0)

Replace any NULL values with reasonable defaults using COALESCE.

## Moving On

NULL is one of those topics that's simple to explain but takes practice to internalize. The mental model is this: NULL means "I don't know." Any comparison with "I don't know" gives you "I don't know." And WHERE only keeps rows where it knows the answer is TRUE.

Next week, we'll look at window functions, which allow you to do advanced aggregation across rows without collapsing them. Running totals, rankings, row comparisons. It's the feature Python developers miss most when they go back to writing loops.