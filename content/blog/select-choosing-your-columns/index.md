---
title: "SELECT: Choosing Your Columns"
description: SQL's SELECT is more than picking columns. Rename with AS, compute expressions, and use DISTINCT for unique values.
author:
  - Jamal Hansen
date: 2026-02-16
tags:
  - sql
categories:
cover:
  image: "erik-mclean-F5G4YTN5uEQ-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Erik Mclean"
    username: "introspectivedsgn"
    photo_id: "white-refrigerator-with-assorted-items-F5G4YTN5uEQ"
draft: false
ShowToc: false
series: "SQL for Python Developers"
layout: post
weight: 7
---

You have written `SELECT *` many times by now. It works, but it's a bit like asking for everything in the fridge when you just want milk. This week, we will look at the `SELECT` clause and see that it does more than just pick columns. It transforms your output.

Previously, we looked closely at [the `FROM` clause](https://jamalhansen.com/blog/from-where-your-data-lives/), which tells the database where the query will find the data. The `SELECT` clause defines which columns will be returned, and you can reshape data on the way out.

## Python Comparison

Let's return to the list comprehension to illustrate how `SELECT` can transform your output. 

```python
# Python: Pick specific keys from dicts
[{'name': c['name'], 'email': c['email']} for c in customers]
```

In this example, we are picking out the name and email elements from the list of customers. This will `SELECT` name and email `FROM` customers.

Now let's look at the SQL:

```sql
SELECT name, email FROM customers
```

Hey, look at that! It does the same thing.

## SELECT *

Before we go further, let's talk about `SELECT *`. It returns every column, and while it's convenient for exploration, it has some downsides.

First, it makes your query harder to read. Someone looking at your code (including future you) has to check the table structure to know what columns come back. Second, if the table structure changes and new columns are added, your query might return data you did not expect. Third, returning columns you do not need wastes resources.

For quick exploration, `SELECT *` is fine. For anything you plan to keep, it's a good idea to list your columns explicitly.

## Beyond Picking Columns

So that's straightforward. `SELECT` lets you pick the columns you want from the table, but I promised you more than that. Let's look at some other things you can do with `SELECT`, like renaming columns and expressions.

### Renaming Columns with AS (Aliases)

The `AS` keyword lets you create your own custom name for a column in the query results. This is called an alias. To make an alias, simply put `AS alias` after the definition of the column that you want to rename.

```sql
SELECT name AS customer_name, email AS contact
FROM customers
```

Output columns are now called `customer_name` and `contact`.

If you are interested in the Python equivalent, it looks like this:

```python
[{'customer_name': c['name'], 'contact': c['email']} for c in customers]
```

### Simple Expressions

You can also write simple expressions to transform data. Two common ways to transform data are to concatenate strings and perform calculations on numbers. Here are some examples using our customers table:

```sql
-- Concatenate strings and alias the result
SELECT name, city || ', USA' AS location
FROM customers

-- Math on numbers
SELECT name, 2026 - YEAR(signup_date) AS years_as_customer
FROM customers

-- Transform text
SELECT name, UPPER(city) AS city_uppercase
FROM customers
```

One thing to watch out for: if any value in your expression is NULL, the whole result becomes NULL. We will dig into why this happens later in the series.

### DISTINCT: Unique Values Only

Another keyword that you will find in the `SELECT` clause is `DISTINCT`. This removes duplicate values from the results. 

```sql
-- All cities (with duplicates)
SELECT city FROM customers

-- Unique cities only
SELECT DISTINCT city FROM customers
```

It is good to understand what this keyword does, but I recommend caution when using it. Using `DISTINCT` can hide duplication caused by a poorly written query. If you find yourself adding `DISTINCT` to fix unexpected duplicates, take a moment to understand why those duplicates appeared in the first place. Sometimes the real fix is elsewhere in your query.

## What's Next

Now you can choose and transform columns using `SELECT`. But you might have noticed something: the rows come back in no particular order. Run the same query twice, and you might get a different row order. Next week, we will look at `ORDER BY`, which gives you control over how your results are sorted.
