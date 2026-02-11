---
title: "HAVING: Filtering Grouped Results"
description: WHERE filters rows before grouping; HAVING filters after. Need "only cities with more than 10 customers"? That's HAVING.
author:
  - Jamal Hansen
date: 2026-03-17
tags:
  - sql
categories:
cover:
  image: "shun-idota-cekJ1XXx1Rk-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "shun idota"
    username: "itzshunnn"
    photo_id: "cars-parked-on-the-side-of-the-road-during-daytime-cekJ1XXx1Rk"
draft: false
ShowToc: false
series: "SQL for Python Developers"
weight: 11
---

When I first encountered HAVING, I thought, "Why do we need this? It's just like WHERE."

Then I tried filtering on COUNT() and hit a strange error. That's when it clicked: `HAVING` filters *after* grouping, not before. It's what you need when WHERE won't work because the thing you want to filter on doesn't exist until after GROUP BY runs.

Let's start with a simple query of customer count by city. But there are a lot of cities and we only care about those with more than ten customers. 

```sql
-- Cities with their customer counts
SELECT city, COUNT(*) as customer_count
FROM customers
GROUP BY city
```

Your first instinct might be to add this to WHERE:

```sql
-- This fails
SELECT city, COUNT(*) as customer_count
FROM customers
WHERE COUNT(*) > 10  -- Error! COUNT doesn't exist yet
GROUP BY city
```

This is when you need `HAVING`. It appears in a different place in the SQL (after the `GROUP BY`), and it executes after the records are grouped. The `WHERE` clause executes before the records are grouped. 

```sql
SELECT city, COUNT(*) as customer_count
FROM customers
GROUP BY city
HAVING COUNT(*) > 10
```

If we were to do this in Python, it would be something like this.

```python
# Python: Filter after grouping
from collections import Counter

city_counts = Counter(c['city'] for c in customers)

# Filter to cities with more than 10
big_cities = {city: count for city, count in city_counts.items() if count > 10}
```

The `if count > 10` part is like HAVING -- it runs after you've counted. In Python, you can filter after counting in the same expression. SQL can't do that because of its clause-based execution model, so it needs a separate keyword.

## Using `WHERE` and `HAVING` Together

We looked at these separately, but in practice you'll almost always use them together. Most real questions require filtering rows first and then filtering the grouped results.

Here is an example to find premium customers only, grouped by city, and only cities with 5+ premium customers. 

```sql
SELECT city, COUNT(*) as premium_count
FROM customers
WHERE is_premium = true      -- Filter rows first
GROUP BY city
HAVING COUNT(*) >= 5         -- Then filter groups
ORDER BY premium_count DESC
```

This SQL runs in the following order...
```
FROM customers           -- 1st: Get data
WHERE is_premium = true  -- 2nd: Filter to premium only
GROUP BY city            -- 3rd: Group by city
HAVING COUNT(*) >= 5     -- 4th: Keep only groups with 5+
SELECT city, COUNT(*)    -- 5th: Pick columns
ORDER BY premium_count   -- 6th: Sort
```

## Alias References in HAVING

One note on `HAVING` and also `GROUP BY` when using them with aliases. Some databases allow you to reference a column by its alias, but this doesn't always work. 

```sql
SELECT city, COUNT(*) as customer_count
FROM customers
GROUP BY city
HAVING customer_count > 10  -- May fail in some databases
```

The reason is that, according to the SQL standard, HAVING runs before SELECT, so the alias technically doesn't exist yet. Some databases like DuckDB relax this rule and allow it, but it's safer to repeat the aggregate for portability.

```sql
SELECT city, COUNT(*) as customer_count
FROM customers
GROUP BY city
HAVING COUNT(*) > 10  -- Always works
```

Building on the [`GROUP BY`](https://jamalhansen.com/blog/group-by-aggregating-your-data) foundations from last week, HAVING unlocks a whole class of questions you couldn't answer before. "Which products sold more than 100 units?" "Which customers made 5+ purchases?" Now you can answer them.

You now have a solid foundation in the core SQL clauses: SELECT, FROM, WHERE, ORDER BY, GROUP BY, and HAVING. But so far we've only worked with one table. Next week: JOINs, combining data from multiple tables.