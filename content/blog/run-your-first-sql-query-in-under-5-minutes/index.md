---
title: "Zero-Setup SQL: Run your first SQL query in under 5 minutes with DuckDB"
summary: Install DuckDB with pip, create your first table, insert data, and run a SQL query - all in Python, all in under 5 minutes, zero configuration required
author:
  - Jamal Hansen
date: 2026-01-10
lastmod: ""
tags:
  - python
  - duckdb
categories:
cover:
    image: five-minutes-wide.jpg
    alt: "Zero-Setup SQL: Run your first SQL query in under 5 minutes with DuckDB"
    relative: true
draft: false
toc: false
series: "SQL for Python Developers"
canonical_url: https://jamalhansen.com/blog/run-your-first-sql-query-in-under-5-minutes
slug: run-your-first-sql-query-in-under-5-minutes
layout: post

---
Have you ever tried setting up a database server just to learn SQL? Docker containers, admin credentials... Forget all that. Let me show you how to go from zero to running SQL in under 5 minutes.

## Why are we using DuckDB to learn SQL? 
- No setup - Just import and start using it
- Real SQL - PostgreSQL compatible syntax so what you learn transfers
- Fast enough - Handles millions of rows on your laptop 
- Python-native - Works well with lists, DataFrames, CSV files 

It is perfect for learning without infrastructure headaches.
## Installation

```shell
pip install duckdb
```

That's it. You're done. No, really.

## Your First Query
Now that we are ready to query the database, let's write our first query and run it. 

```python
import duckdb

# Connect to DuckDB
with duckdb.connect(':memory:') as con:
	# Create table
	con.execute("""
	    CREATE TABLE data(name VARCHAR, score INTEGER)
	""")
	
	# Insert data
	con.executemany(
	    "INSERT INTO data VALUES (?, ?)",
	    [('Alice', 95), ('Bob', 87), ('Carol', 92)]
	)
	
	# Query the data
	result = con.execute("""
	    SELECT name, score 
	    FROM data 
	""").fetchall()

print(result)
```

When you run this, you should see the result:
```bash
[('Alice', 95), ('Bob', 87), ('Carol', 92)]
```

## What happened?

So what exactly is [DuckDB](https://duckdb.org "The homepage for DuckDB"), and what did we do in these 22 lines of code? 

**DuckDB** is an embedded SQL database optimized for analytics. Think "SQLite for data analysis". It runs inside your Python process with zero setup. 

Our 22-line script did four things: 
1. Connect - Created an in-memory database (`:memory:`) 
2. Create - Defined a table structure (name + score) 
3. Insert - Added three rows of data 
4. Query - Retrieved scores from the database

This is the basic SQL workflow you'll use everywhere. Often, steps 2 and 3 aren't necessary because someone else already did them for you.

## Try It Yourself

Want to experiment? Modify the query to:
- Get only scores above 90: Add `WHERE score > 90`
- See the highest score first: Add `ORDER BY score DESC`
- Get just the top scorer: Add `LIMIT 1`

The best way to learn SQL is by experimenting. Try these modifications and see what happens!
## What You Just Learned

In 5 minutes, you:
- Installed a production-grade SQL database
- Created your first table
- Inserted data
- Wrote your first SELECT query

No servers. No complexity. Just SQL.

Next week, we will use Python's `faker` library to generate realistic datasets and practice SQL on hundreds of rows. You'll see why data folks love SQL for exploration.
