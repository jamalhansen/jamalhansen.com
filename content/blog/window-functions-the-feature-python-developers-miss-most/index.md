---
title: "Window Functions: The Feature Python Developers Miss Most"
description: Calculate across rows without collapsing them. Running totals, rankings, and row comparisons that GROUP BY can't do.
author:
  - Jamal Hansen
date: 2026-04-20
tags:
  - sql
categories:
cover:
  image: "r-mo-w-_iZqdviAo-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "R Mo"
    username: "mooo3721"
    photo_id: "calm-body-of-water-near-brown-mountain-under-white-and-gray-sky-w-_iZqdviAo"
draft: false
ShowToc: false
series: "SQL for Python Developers"
weight: 16
---
This week, we are going to focus on window functions, which are very powerful data manipulation tools. It's something that you can do in Python, but in SQL, it is super simple and very powerful. We'll continue using the same `orders` and `customers` tables from [previous posts](https://jamalhansen.com/blog/where-filtering-your-data) in our DuckDB sample database.

Before I continue, I have a confession to make. While I have used window functions, I haven't used them nearly as much as I should have. I only discovered them in the past few years. Prior to that, I used some other SQL tricks for these types of queries, but this method is much cleaner. 

So let's dive in. What problem do window functions solve? They seem to do aggregation-type activities, can't `GROUP BY` do this? 

The short answer is, not very well. 

Window functions allow you to do things like calculate running totals, rankings, and moving averages, which tend to be very difficult to do otherwise because it requires a 'window' into a subset of the data. 

## The Problem GROUP BY Can't Solve

So let's look at a simple grouped query. This is each customer id and the total amount ordered for that customer. The `GROUP BY` allows the aggregation by customer id.

```sql
SELECT customer_id, SUM(amount) as total
FROM orders
GROUP BY customer_id
```

But what if you want:
- Each order row, *plus* the customer's running total at that point?
- Each order row, *plus* how it compares to the average?
- Each order row, *plus* its rank within that customer's orders?

GROUP BY can't do this, but window functions can.

## Python Comparison

Looking at a Python-based alternative, Pandas handles this reasonably well, though you have to bring back all the data unsummarized for it to do it. 

```python
df['running_total'] = df.groupby('customer_id')['amount'].cumsum()
df['rank'] = df.groupby('customer_id')['amount'].rank(ascending=False)
```

Without Pandas, it's quite tedious to loop and summarize the data.

Now let's look at a window function.

```sql
SELECT *,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) as running_total,
       RANK() OVER (PARTITION BY customer_id ORDER BY amount DESC) as rank
FROM orders
```

Here we will return all orders with the associated cumulative order amount, by date no less. It also ranks the amount of the purchase against the customer's other purchases. Pretty powerful!

## Syntax

Let's take a closer look at the window function syntax. There are two parameters. First is the `PARTITION BY` column, which is similar to `GROUP BY` since it says which column to focus the activity on, except that it doesn't collapse down the data. The second parameter is `ORDER BY` column, which is the order of the data in the partition. Very important for ranks, and running totals. 

```sql
function() OVER (
    PARTITION BY column    -- Like GROUP BY, but doesn't collapse
    ORDER BY column        -- Order within each partition
)
```

## Essential Window Functions

Now, let's go through some valuable window functions that are available. 

Use `ROW_NUMBER()` to get a unique number for each row in the window.
```sql
SELECT name, city,
       ROW_NUMBER() OVER (ORDER BY signup_date) as signup_order
FROM customers
```

Both `RANK()` and `DENSE_RANK()` are available for ranking data. The difference is the way that they handle ties in the data. If two numbers have the same ranking (1, 2, 2, 4), `RANK()` will skip the next value and resume counting. `DENSE_RANK()` does not do this and would rank these as (1, 2, 2, 3).

```sql
SELECT customer_id, amount,
       RANK() OVER (ORDER BY amount DESC) as rank,
       DENSE_RANK() OVER (ORDER BY amount DESC) as dense_rank
FROM orders
```

We are familiar with `SUM()`, `AVG()`, and `COUNT()` as aggregate functions. These are also available as window functions, allowing them to be used over a partition. 
```sql
SELECT customer_id, order_date, amount,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) as running_total,
       AVG(amount) OVER (PARTITION BY customer_id) as customer_avg
FROM orders
```

`LAG()` and `LEAD()` allow you to reference data from the previous or next row in the result set. 
```sql
SELECT customer_id, order_date, amount,
       LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_date) as prev_amount,
       LEAD(amount) OVER (PARTITION BY customer_id ORDER BY order_date) as next_amount
FROM orders
```

## Practical Examples

Now, let's look at some practical examples of how these window functions can be used. 

### Top 3 Orders Per Customer

Here is a simple query that combines CTEs with window functions to return the top three largest orders for each customer.
```sql
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY amount DESC) as rn
    FROM orders
)
SELECT * FROM ranked WHERE rn <= 3
```

### Change Over Time

Here is another useful application of window functions. Here we are comparing the results to the previous time period and determining the difference. 

```sql
SELECT order_date, amount,
       LAG(amount) OVER (ORDER BY order_date) as prev_amount,
       amount - LAG(amount) OVER (ORDER BY order_date) as change
FROM orders
```

## Try It Yourself

### Challenge 1: Find Each Customer's Most Recent Order

Use `ROW_NUMBER()` with a CTE to return only the most recent order for each customer. You'll need to partition by `customer_id` and order by `order_date DESC`.

### Challenge 2: Month-Over-Month Change

Using `LAG()`, write a query that calculates the difference in order amount compared to the previous order for each customer. Partition by `customer_id` and order by `order_date`.

## What's Next?

It's time to set you free to work on your own data and tables. We have seen that briefly already, and next week we are going to take a closer look at SQL's Data Definition Language (DDL) that lets you create tables.