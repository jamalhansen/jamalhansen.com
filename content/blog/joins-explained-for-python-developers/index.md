---
title: JOINs Explained for Python Developers
description: Connect related tables like looking up values in a Python dictionary. Covers INNER JOIN, LEFT JOIN, and when to use each.
author:
  - Jamal Hansen
date: 2026-03-24
tags:
  - sql
categories:
cover:
  image: "duy-pham-Cecb0_8Hx-o-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "unsplash_user:"
    username: "weight: 12"
    photo_id: "unsplash_name:"
draft: false
ShowToc: false
series: "SQL for Python Developers"
weight: 12
---
So far in this series we have covered all the core SQL clauses: SELECT, FROM, WHERE, GROUP BY, HAVING, and ORDER BY. We can do quite a bit with those tools, but we have been working with a single table. SQL is the language of *relational* databases, and it is time to talk about the relational part.

`JOIN`s connect related tables. It's like looking up values in a Python dictionary or merging pandas DataFrames, except that the database handles the matching. Today we are going to see how this works, but first we need a little setup.

## Setup: The Orders Table

Relational databases organize concepts into tables. So far, we have seen this in action with our customer table, which stores all sorts of information about customers.

Most databases have more than one table because they model more than one concept. For instance, when you talk about customers, you are talking about their orders as well.  

We could add information about the orders to the customer table, but this has some drawbacks that we will talk about in a minute, so to begin, let's create a separate orders table. 

```python
# Generate orders (add to practice.duckdb)
from faker import Faker
import duckdb
import random

fake = Faker()
Faker.seed(42)
random.seed(42)

con = duckdb.connect('practice.duckdb')

# Create orders table
con.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER,
        customer_id INTEGER,
        product VARCHAR,
        amount DECIMAL(10,2),
        order_date DATE
    )
""")

products = ['Widget', 'Gadget', 'Gizmo', 'Thingamajig', 'Doohickey']

orders = []
for i in range(1000):
    orders.append((
        i + 1,
        random.randint(1, 500),  # Links to customer id
        random.choice(products),
        round(random.uniform(10, 500), 2),
        fake.date_between(start_date='-1y', end_date='today')
    ))

con.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", orders)
```

Great! We have two tables now, one for customers and one for orders. Now, let's look at why we put them in separate tables rather than the same one. 

## The Problem JOINs Solve

Relational databases solve two problems: storage efficiency and data consistency. Let's consider a company with 100 customers and each customer orders, say, once a month. 

If we were to store all of that data in one table, in a year, we would have 12,000 records (12 x 100). Each record would contain the customer's name, address, and related data. It would also contain the information about the ordered item. That means that we now have each customer's data in the table 12 times, which is a waste of space.

Worse than wasting space, it can cause problems too:
- What if the data is different in each record?
- How do you know which is correct?

Relational databases solve this by only storing one copy of the customer data and one copy of each order. They also provide a way to stitch this data together when you want to see both. 

## Enter The `JOIN`

`JOIN`s let you stitch data from multiple tables together when you query. The data is still stored separately, but the query will return the data together. 

You may have noticed the `id` column that we have included in the tables. This column is called a `PRIMARY KEY`, and it is one of the most important concepts in relational databases. The `PRIMARY KEY` uniquely identifies each record in a table. You will encounter this term constantly when working with databases, so it is worth committing to memory.

When a table needs to reference a record in another table, it stores that record's `PRIMARY KEY` rather than copying all of the data. This reference column is called a `FOREIGN KEY`. Together, primary keys and foreign keys are the backbone of how relational databases connect data.

Let's take a look at the orders table we just created. Notice that it has an `id` and a `customer_id` column. The `id` column is the primary key for orders. The `customer_id` is a foreign key that points to the `id` column in the customer table.

```sql
-- Orders table has customer_id, but not customer name
SELECT * 
FROM orders 
LIMIT 5
-- id | customer_id | product | amount | order_date
-- 1  | 247         | Widget  | 89.99  | 2025-06-15
```

If we were to join data in Python it would look something like this. 
```python
# You have two lists, need to combine by matching ID
customers = [{'id': 1, 'name': 'Alice'}, ...]
orders = [{'id': 1, 'customer_id': 1, 'product': 'Widget'}, ...]

# Linear scan -- works, but slow
for order in orders:
    customer = next(c for c in customers if c['id'] == order['customer_id'])
    print(f"{customer['name']} ordered {order['product']}")

# A dictionary lookup would be faster, and that's closer to what SQL does
customers_by_id = {c['id']: c for c in customers}
for order in orders:
    customer = customers_by_id[order['customer_id']]
    print(f"{customer['name']} ordered {order['product']}")
```

In SQL, remember we use declarative syntax, so we don't have to tell it how to `JOIN`, just what columns to `JOIN` on. JOINs do this matching for you efficiently.

To specify the JOIN, we use the `FROM` clause, and after we tell it the table we want data from, we use the `JOIN` and `ON` keywords to tell the other table as well as the keys to join on.

```sql
SELECT 
	customers.name, 
	orders.product, 
	orders.amount
FROM 
	orders JOIN 
	customers ON orders.customer_id = customers.id
```

This is a basic join, also known as an inner join. 

- `FROM orders` — start with orders table
- `JOIN customers` — bring in customers table
- `ON orders.customer_id = customers.id` — the matching condition

What is important to remember about `INNER JOIN`s is that only rows with matches in *both* tables appear in the results. So if there is a customer with no orders, we would not see them in this query. 

Similarly, if there was an order without a customer associated, it would not be returned by an `INNER JOIN`. We shouldn't have an order without a customer, but it may have been deleted or may just be bad data. 

## Table Aliases

Before we go further, let me introduce one of my favorite features of SQL: the table alias. You may have noticed that typing out full table names like `customers.name` and `orders.product` gets verbose fast. Table aliases let you reference a table with an abbreviated name, usually just a single letter.

```sql
-- Without aliases (verbose)
SELECT customers.name, orders.product
FROM customers
JOIN orders ON customers.id = orders.customer_id
```

Here we see the same query using aliases, which makes it easier to type and easier to read.

```sql
-- With aliases (cleaner)
SELECT c.name, o.product
FROM customers c
JOIN orders o ON c.id = o.customer_id
```

I recommend using just the first letter or two of the actual table name. It just has to be unique and make you think of the table when you see it. This is the best way I've found.

Sometimes you will see sequential letters, numbers, or both used as aliases. I try to avoid this because they aren't meaningful and just make the SQL more difficult to read. 

We will use aliases for the rest of this post, and you will see them everywhere in real-world SQL.

## LEFT JOIN

We just looked at an `INNER JOIN`, but there is another type of join that you will use frequently. The `INNER JOIN` only returns rows that match in both tables, but what if you want to find customers who have *never* placed an order? An `INNER JOIN` would exclude them entirely since there is nothing to match on.

This is where the `LEFT JOIN` (also called `LEFT OUTER JOIN`) comes in. It returns all rows from the table on the left and any matching rows from the table on the right. If there are no records that match, the data for the right table will be returned as `NULL`.

```sql
SELECT 
	c.name, 
	o.product
FROM 
	customers c LEFT JOIN 
	orders o ON c.id = o.customer_id
```

This query returns every record in the customer table, even those that have not ordered. For customers without orders, the `o.product` column will show `NULL`.

Between `INNER JOIN` and `LEFT JOIN`, you will cover the vast majority of your use cases. There are other types like `RIGHT JOIN` and `FULL OUTER JOIN`, but you will rarely need them in practice.

## A Word of Caution

One final note on joins. There may be a time when you get way more results from your join than you expected. Sometimes in the order of millions or billions of rows. Sometimes the database will struggle to return all of the rows in the results to you because there are too many results. 

This issue is probably caused by a `CARTESIAN JOIN`, which is caused by an error in your join. Usually, it happens when you reference multiple tables in your FROM clause without specifying how they connect. This causes each row in one table to be multiplied by each row in the other table, which is almost always a bad thing. 

If you see an unexplained lag in your query or an unexpected number of rows in your result, check your joins and see if there is an issue to fix. 

Finally, I cautioned earlier about using the `DISTINCT` keyword and this is the reason why. If you use `DISTINCT`, you can hide a `CARTESIAN JOIN` that is eating up your database's resources. 

## Practical Examples

Here are a couple more examples of SQL joins. First up, a customer order summary showing the number of orders and total spent for each customer. 
```sql
SELECT 
	c.name, 
	COUNT(o.id) as order_count, 
	SUM(o.amount) as total_spent
FROM 
	customers c LEFT JOIN 
	orders o ON c.id = o.customer_id
GROUP BY 
	c.id, 
	c.name
ORDER BY 
	total_spent DESC
```

We can also find customers with no orders. This is the LEFT JOIN pattern from earlier in action, and it is one you will reach for often.

```sql
SELECT 
	c.name, 
	c.email
FROM 
	customers c LEFT JOIN 
	orders o ON c.id = o.customer_id
WHERE 
	o.id IS NULL
```

You have now unlocked the power of relational databases with `JOIN`s. They can take a little bit of time and practice to master so take a minute and try out a few queries. Here are some queries you can try:

- List all customers who have never placed an order
- Count how many customers have ordered each product
- Find the most popular product in each state

Good luck!

This week, we used JOINs to combine tables. But sometimes you need a query *inside* another query. Next week, we will look at subqueries, which are like nested function calls for SQL.