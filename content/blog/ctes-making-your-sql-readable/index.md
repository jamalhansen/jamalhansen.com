---
title: "CTEs: Making Your SQL Readable"
description: WITH clauses let you name your subqueries and read top-to-bottom instead of inside-out. Transform nested spaghetti into clean steps.
author:
  - Jamal Hansen
date: 2026-04-06
tags:
  - sql
categories:
cover:
  image: "melissa-walker-horn-U7bOjNIqisM-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Melissa Walker Horn"
    username: "sugercoatit"
    photo_id: "a-row-of-yellow-rubber-ducks-on-a-blue-background-U7bOjNIqisM"
draft: false
ShowToc: false
series: "SQL for Python Developers"
weight: 14
---
We learned last week about [subqueries](https://jamalhansen.com/blog/subqueries-when-sql-needs-helper-functions), which are like helper functions for your SQL code. They can bring back temporary values used in larger calculations or find additional data points from an id. 

While subqueries are very powerful, they do add complexity to your code. This complexity adds to the cognitive load when trying to read and understand your code. 

I've been the person who has to dust off an old piece of SQL code that has been running in production for years and just recently started returning invalid rows or experiencing massive latency. 

Usually, the cause is a seemingly unrelated change that broke some assumption in the logic. It's very easy to fix. Except that I have to understand the full script before I can make that simple change. 

When the query is loaded with complex subqueries, the time it takes to understand it is longer than I care to spend. Compounding the problem is that half an hour into the process I get frustrated and decide to contact the original developer for an explanation. A look at the change record shows that I wrote it, and I can't remember why. 

Yes, this has happened to me, more than once. 

Thankfully, there is a SQL feature called a Common Table Expression (CTE) that lets you extract your subqueries and define them with meaningful names, decreasing the cognitive load and making things easier on the future developer who has to understand your code.

## An Example

Here is some SQL with nested subqueries. It's not even a very complex example. Still, it takes a minute (or more) to understand the intent.

```sql
SELECT city, order_count FROM (
    SELECT c.city, COUNT(*) as order_count
    FROM customers c
    JOIN (
        SELECT customer_id, amount 
        FROM orders 
        WHERE amount > (SELECT AVG(amount) FROM orders)
    ) big_orders ON c.id = big_orders.customer_id
    GROUP BY c.city
) city_stats
WHERE order_count > 5
ORDER BY order_count DESC
```

You have to read it inside-out, starting with the innermost subquery to get the gist. 

This one gets cities and the associated order count for cities with more than five big orders. I think. 

Common Table Expressions add the `WITH` keyword that allows you to define and name queries. In this case, we define and name `big_orders` and `city_stats`.

```sql
WITH big_orders AS (
    SELECT customer_id, amount 
    FROM orders 
    WHERE amount > (SELECT AVG(amount) FROM orders)
),
city_stats AS (
    SELECT c.city, COUNT(*) as order_count
    FROM customers c
    JOIN big_orders ON c.id = big_orders.customer_id
    GROUP BY c.city
)
SELECT city, order_count 
FROM city_stats
WHERE order_count > 5
ORDER BY order_count DESC
```

Now you can read the query from top to bottom, and the final query is greatly simplified. Success!

## The Python Equivalent

As a Python programmer, this kind of refactoring should feel familiar. You wouldn't write all of your logic in a single nested expression.

```python
# Hard to follow: everything jammed into one expression
result = sorted(
    [(city, count) for city, count in 
        {c['city']: sum(1 for o in orders 
            if o['customer_id'] == c['id'] 
            and o['amount'] > sum(o2['amount'] for o2 in orders) / len(orders))
         for c in customers}.items()
     if count > 5],
    key=lambda x: x[1], reverse=True
)
```

Nobody writes Python like that. You break it into named steps.

```python
# Clear: named intermediate steps
avg_amount = sum(o['amount'] for o in orders) / len(orders)

big_orders = [o for o in orders if o['amount'] > avg_amount]

city_counts = {}
for order in big_orders:
    customer = next(c for c in customers if c['id'] == order['customer_id'])
    city_counts[customer['city']] = city_counts.get(customer['city'], 0) + 1

result = [(city, count) for city, count in city_counts.items() if count > 5]
result.sort(key=lambda x: x[1], reverse=True)
```

CTEs are the SQL version of extracting named intermediate variables for clarity. Same instinct, different syntax.

## Syntax

The SQL syntax for CTEs is:

```sql
WITH cte_name AS (
    -- query here
),
another_cte AS (
    -- can reference cte_name
)
SELECT * FROM another_cte
```

- Start with `WITH`
- Name each CTE
- Separate multiple CTEs with commas
- The final SELECT uses the CTEs

## Building a Data Pipeline

Where CTEs really shine is when you have multiple logical steps. Each CTE builds on the previous one, like a data pipeline.

```sql
WITH 
-- Step 1: Recent orders only
recent_orders AS (
    SELECT * FROM orders
    WHERE order_date >= '2025-01-01'
),
-- Step 2: Aggregate by customer
customer_summary AS (
    SELECT customer_id, 
           COUNT(*) as order_count, 
           SUM(amount) as total_spent
    FROM recent_orders
    GROUP BY customer_id
),
-- Step 3: Add customer details
enriched AS (
    SELECT c.name, c.city, cs.order_count, cs.total_spent
    FROM customers c
    JOIN customer_summary cs ON c.id = cs.customer_id
)
-- Final: Filter and sort
SELECT * FROM enriched
WHERE total_spent > 500
ORDER BY total_spent DESC
```

Each step is testable on its own. Want to see what `recent_orders` looks like? Just run `SELECT * FROM recent_orders` temporarily and check the results before you move on.

## Try It Yourself

These challenges are made for our customers and orders sample database.

### Challenge 1: Customer Order Summary

Rewrite this nested subquery as a CTE:

```sql
SELECT name, total_spent FROM (
    SELECT c.name, SUM(o.amount) as total_spent
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    GROUP BY c.id, c.name
) customer_totals
WHERE total_spent > 500
ORDER BY total_spent DESC
```

Then extend it: add `order_count` and filter to customers with 3+ orders.

### Challenge 2: Multi-Step Pipeline

Build a CTE pipeline from scratch:

- **Step 1**: Define a CTE for each customer's total spent and order count
- **Step 2**: Define a CTE that joins customer details (name, city) to those totals
- **Step 3**: In your final SELECT, filter to customers with above-average total spending

Hint: you can use a subquery inside a CTE for the average, or define it as its own CTE.

### Challenge 3: Reuse a CTE

Write a query with a single CTE called `customer_totals` (customer_id, order_count, total_spent), then use it twice in the final SELECT: once to get the top 5 spenders and once to get the bottom 5. You can use `UNION ALL` to combine them.

## Moving On

You've now got a solid querying toolkit. You can filter, join, aggregate, nest subqueries, and organize complex logic with CTEs. That covers a lot of what you'll use day to day.

But there's a topic that trips up every SQL developer eventually, often in sneaky ways. It's a value that isn't equal to anything, not even itself. Next week, we'll discuss NULL.