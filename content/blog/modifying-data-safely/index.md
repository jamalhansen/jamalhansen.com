---
title: Modifying Data Safely
description: INSERT, UPDATE, and DELETE with guardrails. Always use WHERE, test with SELECT first, and use transactions to undo mistakes.
author:
  - Jamal Hansen
date: 2026-05-04
tags:
  - sql
categories:
cover:
  image: "edwin-hooper-TJ9rBJAAguQ-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Edwin Hooper"
    username: "edwinhooper"
    photo_id: "red-and-white-stop-road-sign-TJ9rBJAAguQ?"
draft: false
ShowToc: false
series: "SQL for Python Developers"
unsplash_user: edwinhooper
---
<!-- test:needs: customers, orders, vip_customers -->

This week, we are going to look at modifying data in a database, and I'll be honest, it can be scary. There is no safety net, no undo button. 

There are some techniques you can use to minimize your risk. We will take a look at them today as we discover how to add, update, and delete data in your database.

## Python Comparison

In Python, modifying a list is forgiving. You can append, reassign, and remove items, and if something goes wrong, your original data is usually still sitting in memory or on disk.

```python
customers = [
    {"name": "Alice", "email": "alice@example.com", "city": "Denver"},
    {"name": "Bob", "email": "bob@example.com", "city": "Austin"},
]

# INSERT is like append
customers.append({"name": "Carol", "email": "carol@example.com", "city": "Seattle"})

# UPDATE is like reassigning a field
customers[1]["city"] = "Houston"

# DELETE is like filtering with a list comprehension
customers = [c for c in customers if c["name"] != "Bob"]
```

The key difference? Python lists live in memory. If you mess up, you restart the script and your source data is fine. SQL modifies the actual stored data. There is no "re-run the script." When you commit a change, it's permanent. That's why the rest of this post is all about guardrails.

## TL;DR The WHERE clause is your friend.

This deletes all of your customers.

```sql
DELETE FROM customers
```

It's been a long day, and you found a duplicate customer record in your customers table. You write some SQL, run it, and your table is now strangely empty. 

You look back at the statement that you ran and see that you ran a `DELETE` statement without a `WHERE` clause, and it removed all the data in your table. 

It's easy to do, and I've done it. 

Let's start by talking about steps that you can take to avoid this scenario. 

The first step is to add a `WHERE` clause to your SQL. 

```sql
DELETE FROM customers
WHERE id = 3
```

This is a great start. We know that `id` is your primary key, so at worst, this will delete one row. 

But how do you know it's the correct record? The simplest way is to transform the SQL into a `SELECT` statement.

Remember what I said about preferring not to use `SELECT *`? This is a situation where it's probably the right choice.

```sql
SELECT * FROM customers
WHERE id = 3
```

When you run this, you will see the row you will delete, and verify that it is correct. Once you have done this, you can feel more confident that the row you will delete is correct. 

## INSERT -- Adding Rows

Now that we have addressed the scary stuff, let's look at how to insert data into our tables.

There are three forms of `INSERT`, and they are used for different reasons. 

The first is a basic insert of a single row of data. While it's not strictly necessary to list the columns that you will be inserting data into, it's a best practice. Notice that the column names and the data are in the same order. 

```sql
INSERT INTO customers (name, email, city)
VALUES ('Alice Smith', 'alice@example.com', 'Denver')
```

If you have multiple rows of data to insert into the same table you can use this form.

```sql
INSERT INTO customers (name, email, city)
VALUES 
    ('Bob Jones', 'bob@example.com', 'Austin'),
    ('Carol White', 'carol@example.com', 'Seattle')
```

Sometimes you want to insert data into a table based on the results of another query. This is especially useful if you are transforming a dataset. Imagine you've created a separate table to track your premium customers.

```sql
INSERT INTO vip_customers (name, email)
SELECT name, email FROM customers WHERE is_premium = true
```

## UPDATE -- Changing Rows

To change data in your table, use an `UPDATE` statement. Here is the basic syntax.

```sql
UPDATE customers
SET city = 'New York'
WHERE id = 42
```

You can update multiple columns at the same time. 

```sql
UPDATE customers
SET city = 'New York', is_premium = true
WHERE id = 42
```

Similar to a `DELETE`, the `WHERE` clause determines how many rows your `UPDATE` will affect. So don't forget your `WHERE` clause. 

```sql
UPDATE customers
SET is_premium = true
WHERE city = 'New York'
```

Before running that UPDATE, use the SELECT-first trick here too. This is especially important when your WHERE clause targets multiple rows.

```sql
-- Step 1: See what you're about to change
SELECT id, name, city, is_premium
FROM customers
WHERE city = 'New York'
```

Check the results. Are those really the 12 customers you wanted to update? Is there a "New York City" variant you're missing? Once you're satisfied, swap the SELECT for your UPDATE.

```sql
-- Step 2: Now update with confidence
UPDATE customers
SET is_premium = true
WHERE city = 'New York'
```

Make this a habit. SELECT first, UPDATE second. Every time.

## Transactions

Another useful tool for ensuring that your updates (or deletes) are accurate is the transaction. If you've used Python context managers or try/except blocks, the concept will feel familiar. They give you a way to try something and back out if it goes wrong. The difference is that instead of catching errors automatically, you inspect the results yourself and decide whether to keep the changes or throw them away.

<!-- test:skip -->
```python
# Python: the concept (not the mechanics)
try:
    do_risky_thing()
    confirm()  # like COMMIT
except:
    undo()     # like ROLLBACK
```

A SQL transaction wraps your changes so that only your session can see them. Nothing is permanent until you say so.

Here's what the workflow looks like. You start the transaction, make your change, and then check the results before deciding.

```sql
BEGIN TRANSACTION;

DELETE FROM orders WHERE order_date < '2023-01-01';

-- Check what happened
SELECT COUNT(*) FROM orders;
```

If the count looks right, make it permanent:

```sql
COMMIT;
```

If something went wrong, undo everything:

<!-- test:expected-failure -->
```sql
ROLLBACK;
```

The key idea is that between `BEGIN` and `COMMIT`, your changes are provisional. In a shared database, other users querying the same table won't see your deletes yet. If you realize you made a mistake, `ROLLBACK` restores everything to the state it was in before your transaction started. DuckDB supports transactions, so you can practice this right now in your local setup.

### Soft Delete Pattern
It may take a little more work, but there is a useful pattern you can use to effectively remove data from your database without deleting it.

If you add a `deleted_at` column to your table, you can then "delete" records by setting a timestamp in that column. 

```sql
-- Instead of deleting, mark as inactive
ALTER TABLE customers ADD COLUMN deleted_at TIMESTAMP;

UPDATE customers SET deleted_at = CURRENT_TIMESTAMP WHERE id = 42;

-- Query only "active" customers
SELECT * FROM customers WHERE deleted_at IS NULL;
```

There are trade-offs to this approach. On the downside, every query against that table now needs a `WHERE deleted_at IS NULL` filter, and you have to remember to add it. You're also keeping rows around that take up storage. For a small table, this doesn't matter, but it adds up at scale.

The benefits usually outweigh those costs. First, if you accidentally soft-delete the wrong records, recovery is a simple UPDATE to set `deleted_at` back to NULL. Compare that to restoring from a backup. Second, you retain historical data. If you're running reports that look at trends over time, hard-deleted records will skew your results because they simply vanish from the dataset.

One tip: if you find yourself adding `WHERE deleted_at IS NULL` to every query, you can create a view (think of it as a saved query) that filters for you automatically. Views are worth looking up on your own once you're comfortable with the basics.

## Try It Yourself

### Challenge 1: Insert and Verify
Using the `customers` table, insert three new customers in a single statement. Then write a SELECT query to verify your new rows exist. Hint: you can filter by name or use `ORDER BY` with a `LIMIT` to see the most recently added rows.

### Challenge 2: Safe Update with SELECT-First
You need to update all customers in `'Austin'` to `'Austin, TX'`. Before running the UPDATE, write the SELECT query that shows exactly which rows will change. How many rows does it affect? Then write the UPDATE.

### Challenge 3: Transaction Rollback
Start a transaction, then delete all orders where `order_date` is older than `'2024-01-01'`. Use `SELECT COUNT(*) FROM orders` to see how many rows remain. Practice using ROLLBACK to undo the delete, then run the same COUNT query again to verify the data is restored.

### Challenge 4: Soft Delete
Add a `deleted_at` column to your `customers` table (you learned ALTER TABLE in the last post). "Delete" a customer by setting `deleted_at` to `CURRENT_TIMESTAMP`. Then write a query that returns only active (non-deleted) customers.

## Next Week

You can now create, query, and modify data in a database. That's quite a lot. Next week, we will tackle a topic that is relatively simple to learn, but can take a lifetime to master. Sometimes your queries can get slow, especially if you have a lot of data in your table. Next time, we will look at optimizing your SQL.
