---
slug: orm-vs-raw-sql-decision-framework
title: "ORM vs Raw SQL: Decision Framework"
description: It's not either/or. Use ORMs for CRUD and migrations; use raw SQL for analytics and complex queries. A practical decision guide.
author:
  - Jamal Hansen
date: 2026-06-01
tags:
  - sql
cover:
  image: "jens-lelie-u0vgcIOQG08-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Jens Lelie"
    username: "madebyjens"
    photo_id: "two-roads-between-trees-u0vgcIOQG08"
draft: false
ShowToc: false
series: "SQL for Python Developers"
unsplash_user: madebyjens
---
<!-- test:needs: customers, orders, salespeople, deals -->

At the [beginning of this series](https://jamalhansen.com/blog/i-know-python-why-learn-sql), I promised that even if you know how to use an Object Relational Mapper (ORM) to interact with a database, knowing SQL would make you a better developer. Now that we have covered everything from SELECT to parameterized queries, it is time to answer the question that every Python developer eventually asks: when should I use an ORM, and when should I just write SQL?

This is one of those topics where everyone has an opinion. I would love to hear yours. Find me on [LinkedIn](https://www.linkedin.com/in/jamalhansen/), [Twitter/X](https://x.com/jamahans), [Bluesky](https://bsky.app/profile/jamalhansen.bsky.social), or [Mastodon](https://techhub.social/@jamalhansen) and let me know where you land after reading this.

## The False Dichotomy

It's not ORM *vs* SQL. Like many choices, each of them does many things well, but with that come a few things that they don't do so well. Optimizing your code comes down to knowing when each shines.

All too often, I see Python developers either use an ORM for everything and miss SQL's power or avoid ORMs entirely, finding out that they have to write a bunch of boilerplate code.

Let's take a look at what each of these tools does well.

## What ORMs Do Well

### CRUD Operations
If you have worked with an application that stores data in a database, you are probably familiar with the term CRUD. It stands for Create, Retrieve, Update, and Delete. Most database-backed applications live and die by these four operations (and REST APIs for that matter).

Using an ORM, creating a user record might look like this:
<!-- test:skip -->
```python
user = User(name="Alice", email="alice@example.com")
session.add(user)
session.commit()
```

Whereas using raw SQL, it would look like this.
<!-- test:skip -->
```python
con.execute("INSERT INTO users (name, email) VALUES (?, ?)", ["Alice", "alice@example.com"])
```

Looking at these two examples, the ORM wins. It's cleaner, more readable, type-safe, and has less boilerplate.

### Schema Migrations
Some ORMs track schema changes and generate migrations to build up or tear down your database. This is a wonderful feature, and I recommend you use it.
```bash
alembic revision --autogenerate -m "add phone column"
alembic upgrade head
```

Managing your DDL SQL separately is tedious. Even if the migration scripts live in the same codebase, keeping them in sync gets painful as your database grows and changes.

### Object Mapping

ORM means Object Relational Mapper. Relational in this phrase is short for relational database, meaning that the ORM maps your data between the database table and an object in your code.

It only makes sense that this is a benefit of ORMs.
<!-- test:skip -->
```python
user = session.query(User).get(42)
user.send_welcome_email()
```
Super clean, and a nice level of abstraction, so it makes your code readable without having to dive into the nuanced details of copying data over and setting values on fields.

SQL doesn't really do this at all. You can pull back the record, but you are on your own to create an object from the data, it will be in a dict or a tuple.
<!-- test:skip -->
```python
row = con.execute("SELECT * FROM users WHERE id = 42").fetchone()
```

So far, it looks like ORMs are the way to go. You might be saying, "But Jamal, I thought you said all this effort was going to be worth my time! Why are you telling me that ORMs are better after all?"

## What Raw SQL Does Well

Okay, ORMs are great, but they don't do everything well. Let's look at some areas where raw SQL really shines.

### Complex Queries

We learned some pretty fancy syntax that SQL uses to manipulate data in all sorts of ways. You can write any complex query in SQL using [joins](https://jamalhansen.com/blog/joins-explained-for-python-developers), [CTEs](https://jamalhansen.com/blog/ctes-making-your-sql-readable), [window functions](https://jamalhansen.com/blog/window-functions-the-feature-python-developers-miss-most), and [subqueries](https://jamalhansen.com/blog/subqueries-when-sql-needs-helper-functions).
```sql
WITH monthly_stats AS (
    SELECT customer_id,
           DATE_TRUNC('month', order_date) as month,
           SUM(amount) as monthly_total,
           LAG(SUM(amount)) OVER (PARTITION BY customer_id ORDER BY DATE_TRUNC('month', order_date)) as prev_month
    FROM orders
    GROUP BY customer_id, DATE_TRUNC('month', order_date)
)
SELECT * FROM monthly_stats WHERE monthly_total > prev_month
```

Try expressing that in ORM query syntax and you will quickly see why SQL exists.

### Analytics and Reporting

Raw SQL is clearer and more powerful for analytics as well. This is the beauty of its declarative syntax. It's almost immediately clear what the following SQL is doing.
```sql
SELECT
    city,
    COUNT(*) as customers,
    COUNT(*) FILTER (WHERE is_premium) as premium_customers,
    ROUND(100.0 * COUNT(*) FILTER (WHERE is_premium) / COUNT(*), 1) as premium_pct
FROM customers
GROUP BY city
ORDER BY customers DESC
```

### Performance-Critical Queries

SQL gives you lower-level access to your database and that gives you the ability to optimize performance. Not unlike finding an area of your Python code that needs optimization and dropping into C code to write something more optimized and much faster. You can use EXPLAIN to find the bottleneck and rewrite a single query, something that is hard to do when the ORM generates the SQL for you.

### Bulk Operations

We saw the power of `executemany()`, allowing you to insert many rows into a database at once. Issuing an `UPDATE` in pure SQL also gives you this ability. When you are looking to create, modify, or delete many rows, SQL is likely the better option.

## How to Decide

When you are staring at a new feature, ask yourself three questions:

**Am I doing basic CRUD?** If you are inserting, updating, or deleting individual records as part of application logic, reach for the ORM. It handles validation, type safety, and object mapping. You will write less code and it will be easier to maintain.

**Am I analyzing or reporting on data?** If you need aggregations, window functions, CTEs, or anything that looks like a report, write SQL. ORMs can technically express some of these queries, but the resulting code is harder to read, harder to debug, and often slower.

**Am I working with many rows at once?** Bulk inserts, batch updates, and large deletes are SQL territory. ORMs tend to process rows one at a time, which gets slow fast. SQL operates on sets, which is what it was designed to do.

If you are still not sure, there is a reliable fallback: if you can describe what you want in a single SQL statement more clearly than in ORM method chains, use SQL.

## The Hybrid Approach

Most real projects use both, and that is the right call. Use the ORM for your application layer: models, CRUD endpoints, and migrations.

<!-- test:skip -->
```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
```

Use raw SQL for your analytics and reporting layer.
```python
def get_user_engagement_report():
    return con.execute("""
        SELECT u.name,
               COUNT(o.id) as orders,
               SUM(o.amount) as total_spent
        FROM users u
        LEFT JOIN orders o ON u.id = o.customer_id
        GROUP BY u.id, u.name
        HAVING COUNT(o.id) > 0
    """).fetchdf()
```

These two can coexist in the same codebase without conflict. Your ORM handles the writes, and your SQL handles the reads that need power.

If you have been following this series with DuckDB, you have already seen this pattern in action. DuckDB is a natural fit for the SQL side of this split: analytics, exploration, and pipeline transformations. Keep your ORM for application data and DuckDB for the analytical heavy lifting.

## Exercises

### Exercise 1: ORM or Raw SQL?

For each of the following scenarios, decide whether you would reach for an ORM or raw SQL, and explain why.

**Hint:** Think about the three questions from the How to Decide section.

a) A user signs up and you need to save their profile.
b) You need a report showing monthly revenue by product category with month-over-month growth.
c) You need to update the email address for a single user.
d) You need to delete all orders older than two years.
e) You need to find the top 10 customers by lifetime value, including their most recent order date.

<details>
<summary>Solution</summary>

a) ORM. Basic insert with validation and type safety.
b) Raw SQL. Aggregations, date functions, and window functions for growth calculations.
c) ORM. Single-record update, benefits from object mapping.
d) Raw SQL. Bulk delete on a date range, no need to load objects into memory.
e) Raw SQL. Aggregation with a subquery or window function for the most recent date.

</details>

### Exercise 2: Refactor to ORM

The following code uses raw SQL to insert a product and its initial inventory. Explain why this would be better handled with an ORM and describe what you would gain.

<!-- test:skip -->
```python
con.execute("INSERT INTO products (name, price, category) VALUES (?, ?, ?)", [name, price, category])
product_id = con.execute("SELECT last_insert_rowid()").fetchone()[0]
con.execute("INSERT INTO inventory (product_id, quantity) VALUES (?, ?)", [product_id, initial_stock])
```

<details>
<summary>Solution</summary>

This is classic CRUD with a relationship between two tables. With an ORM, it might look something like this:

<!-- test:skip -->
```python
product = Product(name=name, price=price, category=category)
product.inventory = Inventory(quantity=initial_stock)
session.add(product)
session.commit()
```

You gain automatic ID management (no manual `last_insert_rowid()`), transaction safety (both inserts succeed or neither does), and code that reads like the business logic it represents.

</details>

### Exercise 3: Build a Dashboard Query

You have been asked to build a dashboard showing each salesperson's total revenue, number of deals, average deal size, and rank within their region. Would you use an ORM or raw SQL? Write the query.

**Hint:** You will need aggregation and a window function for ranking.

<details>
<summary>Solution</summary>

Raw SQL. This needs aggregation and a window function, which is exactly the kind of query ORMs struggle with.

```sql
SELECT
    s.name,
    s.region,
    COUNT(d.id) as deals,
    SUM(d.amount) as total_revenue,
    ROUND(AVG(d.amount), 2) as avg_deal_size,
    RANK() OVER (PARTITION BY s.region ORDER BY SUM(d.amount) DESC) as region_rank
FROM salespeople s
JOIN deals d ON s.id = d.salesperson_id
GROUP BY s.id, s.name, s.region
ORDER BY s.region, region_rank
```

</details>

## Next Week

You can write SQL well, but how do you test it? Next week, we will take a look at testing SQL code: unit tests, fixtures, and validation.