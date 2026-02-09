---
title: "GROUP BY: Aggregating Your Data"
description: GROUP BY creates buckets and counts them. It's like Python's `collections.Counter` or pandas `groupby()`. Learn COUNT, SUM, AVG, MIN, and MAX.
author:
  - Jamal Hansen
date: 2026-03-09
tags:
  - sql
categories:
cover:
  image: "alexander-schimmeck-2zJhA9RSkys-unsplash"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Alexander Schimmeck"
    username: "alschim"
    photo_id: "red-and-green-apples-on-red-plastic-crate-2zJhA9RSkys"
draft: false
ShowToc: false
series: "SQL for Python Developers"
weight: 10
---
Last week, we learned to use [`WHERE`](https://jamalhansen.com/blog/where-filtering-your-data) to efficiently return only the rows that we want from a database. But what if you want to summarize the data more efficiently?

It turns out that you can have the database do the summarization for you with the `GROUP BY` keyword.

Like Python's `collections.Counter` or pandas `groupby()`, SQL's GROUP BY lets you summarize data by category. It allows you to count, sum, and average across groups.

## The Problem

At this point, if you were asked how many customers are in the city of San Antonio, you might reach for `ORDER BY` and order by the city, then count the results for San Antonio. 
```sql
SELECT city 
FROM customers
ORDER BY city
```
You might also use a `WHERE` clause and set `city = 'San Antonio'`, return the results, and count the number of rows. This seems more optimized since you will return only the rows where the city is San Antonio

```sql
SELECT city 
FROM customers
WHERE city = 'San Antonio'
```

Neither of these is efficient because what you are looking for is a simple count rather than multiple rows. 

These approaches would be even less effective if you wanted to know the number of customers in each city.
## Python Comparison
Let's take a moment to look at how we might get the number of customers in each city using Python. You could use `Counter`, manual grouping, or `Pandas` to achieve this. 

Here we can see this achieved with a counter
```python
from collections import Counter
city_counts = Counter(c['city'] for c in customers)
```

Here is a manual grouping
```python
city_counts = {}
for c in customers:
    city = c['city']
    city_counts[city] = city_counts.get(city, 0) + 1
```

and Pandas
```python
import pandas as pd
df = pd.DataFrame(customers)
df.groupby('city').size()
```

The issue with all of these solutions is that if you simply want to know how many customers are in each city, you are sending all 500 records to Python and letting it manage them. This gets to be even more of an issue if you have 1 million customers. 

Thankfully, SQL can do this in the database and simply return results that contain the city and the number of customers in that city.
```sql
-- SQL: GROUP BY with COUNT
SELECT city, COUNT(*) as customer_count
FROM customers
GROUP BY city
```

Same result, but the work happens on the database server.
## Aggregate Functions

In this example, `COUNT()` is a function that aggregates values in the query. In this case, it counts them, but there are many aggregate functions in SQL. 

Here are some common ones:

| Function | What it does | Example |
|----------|--------------|---------|
| COUNT(*) | Count all rows | How many customers? |
| COUNT(column) | Count non-NULL values | How many have emails? |
| SUM(column) | Add up values | Total sales |
| AVG(column) | Average value | Average order size |
| MIN(column) | Smallest value | First signup date |
| MAX(column) | Largest value | Most recent signup |

One thing to note: `COUNT(*)` counts all rows, while `COUNT(column)` only counts rows where that column is not NULL. This distinction matters when your data has missing values.

## The Golden Rule
Aggregate functions are very useful, and they work well with the `GROUP BY` clause. There is one thing to remember when using them that will trip you up, even after years of writing SQL. If you are receiving errors or unexpected results when using aggregate functions and `GROUP BY`, this is the first thing that you should check, twice.

**Every column in SELECT must be either:**
1. In the GROUP BY clause, OR
2. Inside an aggregate function

```sql
-- ✅ Correct: city is in GROUP BY, COUNT is aggregate
SELECT city, COUNT(*)
FROM customers
GROUP BY city

-- ❌ Wrong: name is not grouped or aggregated
SELECT city, name, COUNT(*)
FROM customers
GROUP BY city
-- Error! Which "name" should it show for each city?
```

This trips up ~~beginners~~ everyone. The database doesn't know which `name` to pick when there are 50 customers in San Antonio, so it either throws an error or gives bad results.
## The Basics
Here are some examples of how you can use aggregate functions and `GROUP BY` together while keeping the golden rule of grouping in mind. 

First, if you just want to know how many rows are in a table you can use the following syntax

```sql
SELECT COUNT(*) as customer_count
FROM customers
```

You can also return the count of customers per city like we saw before. 

```sql
SELECT city, COUNT(*) as customer_count
FROM customers
GROUP BY city
```

You can also use multiple aggregate functions for the same `GROUP BY`

```sql
SELECT city, 
       COUNT(*) as total,
       MIN(signup_date) as first_signup,
       MAX(signup_date) as last_signup
FROM customers
GROUP BY city
```

..or `GROUP BY` multiple columns

```sql
SELECT city, is_premium, COUNT(*) as count
FROM customers
GROUP BY city, is_premium
```

Notice that in both these examples any column in the `SELECT` clause that is not an aggregate function is in the `GROUP BY` clause.
## Combining with WHERE and ORDER BY

So how does the database handle using a `WHERE` or `ORDER BY` with a `GROUP BY`? 

`WHERE` filters *before* grouping:

```sql
-- Count premium customers per city
SELECT city, COUNT(*) as premium_count
FROM customers
WHERE is_premium = true
GROUP BY city
```

The `ORDER BY` clause sorts the grouped results:

```sql
-- Cities with most customers first
SELECT city, COUNT(*) as customer_count
FROM customers
GROUP BY city
ORDER BY customer_count DESC
```

Below is the execution order, remember that this does not match the order that you write them in a SQL query.

```
FROM customers           -- 1st: Get data
WHERE is_premium = true  -- 2nd: Filter rows
GROUP BY city            -- 3rd: Group remaining rows
SELECT city, COUNT(*)    -- 4th: Pick columns and aggregate
ORDER BY premium_count   -- 5th: Sort results
```

`GROUP BY` lets you count and summarize. But what if you want to filter *after* grouping? For instance, "only return cities with more than 10 customers"? WHERE won't work, and we need a new keyword that we will discuss next week.
