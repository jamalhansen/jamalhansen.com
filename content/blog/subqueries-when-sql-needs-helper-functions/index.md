---
title: "Subqueries: When SQL Needs Helper Functions"
description: Nest queries inside queries, like Python helper functions. Use them in WHERE, SELECT, or FROM to compute intermediate results.
author:
  - Jamal Hansen
date: 2026-03-31
tags:
  - sql
categories:
cover:
  image: "didssph-PB80D_B4g7c-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Didssph"
    username: "didsss"
    photo_id: "red-blue-and-yellow-ceramic-figurine-PB80D_B4g7c"
draft: false
ShowToc: false
series: "SQL for Python Developers"
weight: 13
---
Last week, we talked about the superpower of relational databases, the ability to join tables to make data storage more efficient. In fact, we have covered much of the syntax that you would use on a daily basis already. But SQL's simplicity hides surprising flexibility. You can model data in many ways, and you can often get the same results with different syntax.

The art of SQL is optimizing your queries so that they run well. This comes with experience, so I encourage you to start playing around with the queries and data we are working with. We will see some of this flexibility with today's topic: subqueries.

Subqueries let you nest queries and use one query's result inside another. They are like helper functions in Python. When a query needs an intermediate result, you can embed another query to compute it.

Let's take a look at how we might do this in Python. Suppose that we had a list of orders and we wanted to find all of the big orders. An order is considered big if its cost exceeds the average order cost.

To do this in Python, you might make a helper function to get the average order cost so that you can filter records against that value. 

```python
# Python: Helper function
def get_average_order_cost():
    return sum(o['amount'] for o in orders) / len(orders)

# Use it in a filter
big_orders = [o for o in orders if o['amount'] > get_average_order_cost()]
```

In SQL, we do something similar, called a subquery. A subquery is just a query that is nested inside another query.

```sql
SELECT *                    -- Outer Query
FROM orders
WHERE 
	amount > (
		SELECT AVG(amount)  -- Subquery
		FROM orders
		)
```

The subquery runs first, returns the average value of an order, and the outer query uses it to filter the rows in the result.

## Types of Subqueries
Because of the flexibility of SQL, there are a number of different types of subqueries that can be used in different situations, depending on your needs.
### Scalar Subquery

One of the primary distinctions of subqueries is the number of rows that it returns. Scalar subqueries return a single value, which is what we saw in the previous example. You'll typically compare them using operators like =, >, or <.

### List Subquery
Of course, if scalar subqueries return a single row of data, it is implied that a subquery can also return multiple rows of data. 

A list subquery will return a single column with multiple rows. This is used in the same way that you might use a list in Python, to store multiple related values. 
```sql
-- Customers who have placed orders
SELECT name 
FROM customers
WHERE 
	id IN (
		SELECT DISTINCT customer_id 
		FROM orders
		)
```

In this example, the subquery returns a list of customer ids from the orders table. This list is used to filter customer records to those customers who have an order. Similar to Python, the `IN` operator is used to determine membership in the list. If you want to find customers who don't have an order, you can use `NOT IN` instead. Try it out!

### Table Subquery
Because a subquery is just a normal query embedded in another query, it can return both multiple rows and columns. This is a table subquery.
```sql
-- Treat subquery result as a table
SELECT city, avg_orders
FROM (
    SELECT c.city, AVG(o.amount) as avg_orders
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    GROUP BY c.city
) city_stats
WHERE avg_orders > 100
```

The results of the subquery are treated like a table, one that you generated on the fly. To reference this table, you must give it an alias. 

In this example, we aliased the table `city_stats` and we are using it to return the average order amount by city, but we are limiting the results to cities whose average order exceeds $100.

## Where Subqueries Can Go

Subqueries are both powerful and flexible. Here is a quick reference for the different clauses where you can use them.

### In WHERE
```sql
SELECT * 
FROM customers
WHERE 
	id IN (
		SELECT customer_id
		FROM orders 
		WHERE amount > 200
	)
```

### In FROM
```sql
SELECT * 
FROM (
    SELECT city, COUNT(*) as customer_count
    FROM customers
    GROUP BY city
) city_summary
WHERE customer_count > 5
```

### In SELECT

Subqueries can also appear in the SELECT clause itself, computing a value for each row. Here, a subquery finds the count of orders for each customer.
```sql
SELECT name,
       (
	       SELECT COUNT(*) 
	       FROM orders 
	       WHERE customer_id = customers.id
	   ) as order_count
FROM customers
```

## Correlated vs Non-Correlated

One thing you will notice about that last subquery in the SELECT clause is that its WHERE clause references values from both the outer query (`customers.id`) and the subquery (`customer_id`). This is called a correlated subquery.

Before this, we only dealt with non-correlated subqueries. These subqueries are independent of the outer query because they do not reference it.
### Non-Correlated
```sql
SELECT * 
FROM orders
WHERE amount > (
		SELECT AVG(amount) 
		FROM orders
	)
```

### Correlated

When your subquery references the outer query, it can do powerful things, but it can also make things a little harder to read and possibly less efficient. This is because the subquery re-executes for every row in the outer query, similar to running a function inside a Python for loop.

In this example, we are revisiting the query that returns orders whose amount is greater than that of the average order. If you look closely, there is a twist. This subquery is correlated to the outer query. It sets the customer id value of the subquery equal to that of the outer query. 

This change makes the query return the orders whose value is greater than *that customer's average order*. Pretty powerful!
```sql
-- Subquery runs once per row (slower, but sometimes necessary)
SELECT * 
FROM orders o1
WHERE amount > (
    SELECT AVG(amount) 
    FROM orders o2 
    WHERE o2.customer_id = o1.customer_id
)
```

### A Note on EXISTS

You'll also run into `EXISTS` and `NOT EXISTS` used with correlated subqueries. Instead of returning data, `EXISTS` simply checks whether the subquery returns any rows at all. It is a common alternative to `IN` for checking related records and can be more efficient with large datasets. We will see more of this in future posts.

## Practice

Here are some SQL problems that you can solve with subqueries. Try these against our sample database!

- Return the names of customers who do not have an order
- Find the names and total order amount of customers whose total spend is more than the average total spend
- Return the most recent order for each customer
- Find customers who have placed at least one order using `EXISTS`

## Next Week

Subqueries are very powerful but can be hard to read at times, especially if they are nested in multiple levels, just like nesting in Python. Next week, we will look at Common Table Expressions (CTEs), which are a way to name and organize your subqueries for readable SQL.