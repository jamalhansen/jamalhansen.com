---
title: "Optimizing Queries: EXPLAIN for Python Developers"
description: Read EXPLAIN output to understand why queries are slow. Learn when to add indexes and when to stop worrying about performance.
author:
  - Jamal Hansen
date: 2026-05-11
tags:
  - sql
categories:
cover:
  image: "florian-steciuk-F7Rl02ir0Gg-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Florian Steciuk"
    username: "flo_stk"
    photo_id: "time-lapse-photography-of-highway-F7Rl02ir0Gg"
draft: false
ShowToc: false
series: "SQL for Python Developers"
unsplash_user: flo_stk
---

As databases grow, queries take longer to run. It's to be expected.

If your queries are consistently slow, the query itself could be the problem.

We talked early in this series about SQL being a declarative language. You tell the database what you want, and it figures out how to get it. But we've also seen that SQL gives you the freedom to do things in many ways, and some of those ways are more efficient than others.

Sometimes, a slow query means you didn't choose the most efficient approach. Other times, your data has simply outgrown the default way the database finds records, and you need to give it a little help.

We will look at how to address both of these scenarios today as we dig into query optimization. This is a topic that can take some time and experience to master, but the basics are straightforward.

## Python Comparison

In Python, when code is slow, you reach for a profiler. `cProfile` shows you which functions took the most time. You can also wrap code in timing calls to measure specific sections.

<!-- test:skip -->
```python
# Python: profile to find bottlenecks
import cProfile
cProfile.run('my_function()')

# Or add timing to a specific section
import time
start = time.time()
result = my_query()
print(f"Took {time.time() - start:.2f}s")
```

SQL has its own version of this: `EXPLAIN`. Instead of showing you which functions are slow, it shows you which steps in the execution plan are doing the most work.

## EXPLAIN

`EXPLAIN` shows the execution plan, which is how the database transforms your query into a series of steps to find and return results.

```sql
EXPLAIN SELECT * FROM customers WHERE city = 'New York'
```

DuckDB example output (simplified for readability):
```
┌───────────────────────────┐
│         EXPLAIN           │
├───────────────────────────┤
│ FILTER                    │
│   city = 'New York'       │
│                           │
│ SEQ_SCAN                  │
│   customers               │
└───────────────────────────┘
```

Here, `SEQ_SCAN` means the database is scanning every row of the table looking for matches. This is fine for small tables, but as the table grows, it gets expensive.

There is also `EXPLAIN ANALYZE`, which goes a step further. While `EXPLAIN` shows you what the database *plans* to do, `EXPLAIN ANALYZE` actually runs the query and reports the real timing for each step. Use `EXPLAIN` to check the plan, and `EXPLAIN ANALYZE` when you want to see actual performance numbers.

```sql
EXPLAIN ANALYZE SELECT * FROM customers WHERE city = 'New York'
```

## Key Things to Look For

The output from EXPLAIN can be difficult to read at first. It is showing you step-by-step how the database will find the data needed to return your results. Here are the most important things to watch for.

### Sequential Scan (SEQ_SCAN)
A sequential scan reads every row in the table looking for matches. Think of it like a Python `for` loop that checks each item in a list. It's the simplest approach, and it works fine when the list is short. When you have millions of rows, it's the first thing to address.

### Index Scan
An index scan uses a pre-built lookup structure to jump directly to matching rows. This is why they're called indexes. Just like the index in the back of a book, a database index lets you look up where specific values live without reading every page. We'll create indexes in a moment.

### Join Types
When your query joins tables (like we learned in the JOINs post), the database picks a strategy for matching rows.

A **Hash Join** builds a lookup table from one side and probes it with the other. If you remember the dictionary lookup pattern from the JOINs post (`customers_by_id = {c['id']: c for c in customers}`), that's exactly what a hash join does. This is fast and is what you will see most often.

A **Nested Loop** is the naive approach: for each row in one table, scan the other table for matches. It's the `for order in orders: for customer in customers` pattern, and it's just as slow as it sounds for large tables. If you see a nested loop on a big table, an index on the join column is usually the fix.

### Filter Placement
Look at where in the plan the filtering happens. Remember when we covered WHERE and talked about filtering rows before they are returned? The same principle applies here. If the database filters early, it has less data to carry through the rest of the plan. If filtering happens late (after a join, for example), the database is doing extra work on rows it will throw away.

## Creating Indexes

Indexes make finding data in a table faster. Without an index, the database has no choice but to scan every row. With an index on a column, the database can jump directly to the rows it needs.

Let's see the difference. First, check the plan without an index:

```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 42;
-- Shows: SEQ_SCAN -- scans all rows
```

Now create an index and check again:

```sql
CREATE INDEX idx_orders_customer ON orders(customer_id);
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 42;
-- Shows: INDEX_SCAN -- jumps directly to matching rows
```

The difference in a small table might be negligible, but with millions of rows, an index scan can be orders of magnitude faster than a sequential scan.

### Analyzing Joins

You can also use `EXPLAIN ANALYZE` on join queries to see how the database handles them. Let's revisit the kind of query that might prompt you to reach for EXPLAIN in the first place:

```sql
EXPLAIN ANALYZE
SELECT c.name, o.amount
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE c.city = 'New York'
```

In the output, look for which table is scanned first and whether indexes are being used on the join columns. Check where the city filter is applied. Is the database filtering customers down to New York before the join, or is it joining everything first and filtering after? Early filtering means less work. If you see a nested loop on a large table without an index, adding an index on the foreign key column (like `customer_id`) is usually the fix.

## Quick Optimization Wins

So what does this all mean? Here are the most common things you can do to speed up a slow query:

1. **Add indexes on WHERE columns** -- the most common fix
2. **Add indexes on JOIN columns** -- foreign keys, especially
3. **Filter early** -- use WHERE to reduce data before JOINs
4. **Select only needed columns** -- avoid SELECT * in production queries
5. **Limit results** -- add LIMIT when exploring

## When to Care

One final word of caution. Just like Python, it's not a good idea to optimize prematurely. If you have three tables with a few hundred rows, don't bother with indexes or `EXPLAIN`. If you have a slow query at that scale, it's probably something off in the query itself.

Once you get up to about a million rows, you should be using `EXPLAIN` on your frequently used or slow queries to understand how to improve them. A good rule of thumb: if your query takes more than a second or two and you're not sure why, that's your signal to reach for EXPLAIN.

If you have slow queries in production or that are slowing down your workflow, investigate!

## Try It Yourself

### Challenge 1: Read an EXPLAIN Plan
Run `EXPLAIN` on a simple query against your `customers` table with a WHERE clause (for example, filtering by city). Look at the output and identify the scan type. Is it a SEQ_SCAN?

### Challenge 2: Before and After an Index
Run `EXPLAIN ANALYZE` on `SELECT * FROM orders WHERE customer_id = 42`. Note the scan type. Then create an index with `CREATE INDEX idx_orders_customer ON orders(customer_id)` and run the same `EXPLAIN ANALYZE` again. What changed in the output? (If you already created the index while reading this post, drop it first with `DROP INDEX idx_orders_customer` and start fresh.)

### Challenge 3: Analyze a JOIN
Run `EXPLAIN ANALYZE` on a query that joins `orders` and `customers`. Identify which table the database scans first and what join strategy it uses (Hash Join or Nested Loop).

## Next Week

You can now write queries, modify data, and diagnose performance problems. That covers a lot of ground. Next week, we are going to put it all together and build a complete pipeline: fetch data from an API, load it into DuckDB, transform it with SQL, and export the results. It's the kind of real-world workflow that makes all of these skills click.
