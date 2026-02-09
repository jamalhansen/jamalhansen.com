---
title: "ORDER BY: Sorting Your Results"
description: SQL returns rows in no guaranteed order. Run the same query twice and you might get different results. ORDER BY gives you control, like Python's sorted() with key functions.
author:
  - Jamal Hansen
date: 2026-02-24
tags:
  - sql
categories:
cover:
  image: "sigmund-yXiLaaYwg_E-unsplash"
  alt: "A spoonful of letters with alphabet soup"
  caption: ""
  relative: true
  credit:
    name: "Sigmund"
    username: "sigmund"
    photo_id: "red-and-white-ceramic-bowl-with-silver-spoon-yXiLaaYwg_E"
draft: false
ShowToc: false
series: "SQL for Python Developers"
weight: 8
---

We now have a firm grasp on how to use [SELECT: Choosing Your Columns](https://jamalhansen.com/blog/select-choosing-your-columns) and [FROM: Where Your Data Lives](https://jamalhansen.com/blog/from-where-your-data-lives) to tell the database where to find data and how to format the columns when it returns it. With this knowledge, we can pull back all of the data from a table in a database. 

There is still a problem with the data that we receive from a query. It can come back in any order. It may return in the same order 9 times out of 10, but there is no guarantee that it will come back in the same order next time. This happens because database engines optimize execution plans based on factors like data volume, indexes, and available memory, and those optimizations can change between queries.

## The Problem

The following query will return all of the customers from the `customers` table, but the order can be different (or not) each time. We just don't know. 

```sql
SELECT name, signup_date FROM customers
```

If order matters, you must specify it.

## Python's sorted() Function

As Python developers, we are familiar with sorting data using the `sorted()` function. In this example, we will sort a list of customer records using the signup_date field.

```python
# Python: sorted() with key function
sorted(customers, key=lambda c: c['signup_date'])
```

If we want to reverse the order, we can specify that we want to do that. 

```python
# Reverse order
sorted(customers, key=lambda c: c['signup_date'], reverse=True)
```

## SQL's ORDER BY Keyword

In SQL, if we want to specify the order of the results, we use the `ORDER BY` keyword. This goes at the end of the query, and logically, it will be executed after the data is retrieved and before the results are sent back. 

```sql
SELECT name, signup_date FROM customers
ORDER BY signup_date
```

The default order is ascending (`ASC`). So if you don't specify an order, it will be ascending. If you would like to reverse the order, specify descending (`DESC`) order.

```sql
-- Reverse order (descending)
SELECT name, signup_date FROM customers
ORDER BY signup_date DESC
```

## Sorting by Multiple Columns

If you would like to specify multiple columns to use in your sort, simply list them all separated by commas. SQL will sort them in that order, giving precedence to the columns listed first.

```sql
-- Sort by city, then by name within each city
SELECT name, city
FROM customers
ORDER BY city, name
```

In Python, you can achieve multi-column sorting using a tuple in your key function:

```python
# Python: multiple keys using tuple
sorted(customers, key=lambda c: (c['city'], c['name']))
```

You can also mix sort directions for different columns. This is useful when you want, for example, the newest dates first but alphabetical order within the same date:

```sql
-- Newest signups first, alphabetically within same date
SELECT name, city, signup_date FROM customers
ORDER BY signup_date DESC, name ASC
```

This is one place where SQL shines. In Python, mixing sort directions requires workarounds like negating numeric values or doing multiple successive sorts:

```python
# Python: mixed directions is awkward
# For strings, you need multiple passes or custom key tricks
from functools import cmp_to_key

def compare(a, b):
    # signup_date descending, name ascending
    if a['signup_date'] != b['signup_date']:
        return -1 if a['signup_date'] > b['signup_date'] else 1
    return -1 if a['name'] < b['name'] else (1 if a['name'] > b['name'] else 0)

sorted(customers, key=cmp_to_key(compare))
```

SQL's `DESC` and `ASC` modifiers per column make this much cleaner.

## Try It Yourself

Using the customers table you created in earlier posts, write a query that displays each customer's name, city, and signup_date, sorted alphabetically by city (A to Z), then by signup_date within each city (oldest first).

## Next Week

You can sort your results, but you're still getting all 500 rows. Next week, we will learn how to filter down your results to just the rows you care about using the `WHERE` keyword.
