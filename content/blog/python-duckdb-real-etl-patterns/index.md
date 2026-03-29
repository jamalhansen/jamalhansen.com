---
title: "Python + DuckDB: Real ETL Patterns"
description: Build a complete pipeline - fetch from an API, load into DuckDB, transform with SQL, export results. A capstone putting it all together.
author:
  - Jamal Hansen
date: 2026-05-18
tags:
  - sql
categories:
cover:
  image: "mike-van-den-bos-jf1EomjlQi0-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Mike van den Bos"
    username: "mike_van_den_bos"
    photo_id: "text-jf1EomjlQi0"
draft: false
ShowToc: false
series: "SQL for Python Developers"
unsplash_user: mike_van_den_bos
---

You've spent 19 posts learning SQL concepts: selecting, filtering, joining, grouping, window functions, and more. Today, you put them all together and build something real: a complete data pipeline that fetches data from an API, loads it into DuckDB, transforms it with SQL, and exports the results.

## What is ETL (and ELT)?

This is a real-world example of a common data engineering pattern. You may have heard of ETL (Extract, Transform, Load), where data is transformed before it reaches its destination. What we are actually building today is the more modern variant, **ELT**: Extract, Load, Transform.

- **Extract**: Get data from somewhere (API, CSV, web)
- **Load**: Put the raw data into a database (DuckDB in our case)
- **Transform**: Clean, reshape, and aggregate using SQL inside the database

The difference matters. In traditional ETL, you transform data in Python before loading it. In ELT, you load the raw data first and then use SQL to transform it in place. ELT is the pattern most modern data workflows use because databases like DuckDB are incredibly fast at transformations, and keeping raw data around means you can always re-transform without re-extracting.

With our toolset, Python handles Extract and Load while SQL handles Transform.

## The Project

This project will be broken down into four steps:
1. Fetch JSON data from a public API
2. Load it into DuckDB
3. Transform with SQL (cleaning, aggregating)
4. Export a summary report

Before we get started, you will need a couple of packages installed. We will use `httpx` to hit an API datasource. If you want to extract the data to parquet format, you will also need `fastparquet`. While not required, parquet is a good file format for storing larger datasets in a file. 

```bash
pip install httpx fastparquet
```

Additionally, you will need `pandas` installed, which you should already have if you have been following along.

## Step 1 (Extract): Fetch Data
First, we will hit API endpoints at JSONPlaceholder to extract users and posts datasets. We will convert these to JSON and then to pandas DataFrames.

<!-- test:skip -->
```python
import httpx
import duckdb
import pandas as pd

# Fetch sample data (JSONPlaceholder API)
response = httpx.get('https://jsonplaceholder.typicode.com/posts')
response.raise_for_status()  # Raise an exception if the request failed
posts = pd.DataFrame(response.json())

response = httpx.get('https://jsonplaceholder.typicode.com/users')
response.raise_for_status()
users = pd.DataFrame(response.json())

print(f"Fetched {len(posts)} posts and {len(users)} users")
```

## Step 2 (Load): Into DuckDB
Next, we will load the DataFrames to DuckDB. Notice that we can reference the pandas DataFrames directly by name in our SQL - DuckDB automatically maps Python DataFrame variable names to table references. No CSV intermediary, no explicit schema definition. 

This might look circular at first glance: `CREATE OR REPLACE TABLE posts AS SELECT * FROM posts`. But DuckDB reads from the Python DataFrame on the right side and creates the database table on the left. The name `posts` resolves to the DataFrame variable in your Python scope.

To finish this step, let's validate that the tables now have the correct number of records in them.

<!-- test:skip -->
```python
con = duckdb.connect('etl_demo.duckdb')

# DuckDB resolves 'posts' and 'users' to the pandas DataFrames above
con.execute("CREATE OR REPLACE TABLE posts AS SELECT * FROM posts")
con.execute("CREATE OR REPLACE TABLE users AS SELECT * FROM users")

print(con.execute("SELECT COUNT(*) FROM posts").fetchone())
print(con.execute("SELECT COUNT(*) FROM users").fetchone())
```

## Step 3 (Transform): SQL Queries
Now, let's transform the data using the SQL that we have learned. We will build two reports: how many posts each user has made, and the average post title length by user. 

<!-- test:skip -->
```python
# Posts per user
posts_per_user = con.execute("""
    SELECT u.name, u.email, COUNT(p.id) as post_count
    FROM users u
    LEFT JOIN posts p ON u.id = p.userId
    GROUP BY u.id, u.name, u.email
    ORDER BY post_count DESC
""").fetchdf()

# Average post title length by user
avg_title_length = con.execute("""
    SELECT u.name, 
           ROUND(AVG(LENGTH(p.title)), 1) as avg_title_length
    FROM users u
    JOIN posts p ON u.id = p.userId
    GROUP BY u.id, u.name
    ORDER BY avg_title_length DESC
""").fetchdf()

print(posts_per_user)
print(avg_title_length)
```

## Step 4 (Export): Save Results

Finally, let's write out the transformed results to files. We have a few options depending on your use case.

**CSV** is the simplest option and great for sharing with non-technical stakeholders or opening in a spreadsheet.

<!-- test:skip -->
```python
from pathlib import Path

Path('reports').mkdir(exist_ok=True)  # Create the directory if needed

posts_per_user.to_csv('reports/posts_per_user.csv', index=False)
avg_title_length.to_csv('reports/avg_title_length.csv', index=False)
```

**JSON** works well when downstream consumers are other applications or web services that expect structured data.

<!-- test:skip -->
```python
posts_per_user.to_json('reports/posts_per_user.json', orient='records')
```

**Parquet** is a column-based binary format that's ideal for larger datasets and feeding results into another data pipeline. This is where the `fastparquet` package we installed earlier comes in.

<!-- test:skip -->
```python
posts_per_user.to_parquet('reports/posts_per_user.parquet')
```

**DuckDB table** - saving back to the database is the right call when this transform feeds into future queries or when you want to keep the results alongside the source data.

<!-- test:skip -->
```python
con.execute("CREATE SCHEMA IF NOT EXISTS reports")
con.execute("""
    CREATE OR REPLACE TABLE reports.posts_per_user AS
    SELECT u.name, u.email, COUNT(p.id) as post_count
    FROM users u
    LEFT JOIN posts p ON u.id = p.userId
    GROUP BY u.id, u.name, u.email
""")
```

## Full Pipeline Script
Here is a script with the full ELT pipeline.

<!-- test:skip -->
```python
import httpx
import duckdb
import pandas as pd
from pathlib import Path

def extract() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fetch data from APIs."""
    posts_response = httpx.get('https://jsonplaceholder.typicode.com/posts')
    posts_response.raise_for_status()
    users_response = httpx.get('https://jsonplaceholder.typicode.com/users')
    users_response.raise_for_status()
    return pd.DataFrame(posts_response.json()), pd.DataFrame(users_response.json())

def load(con: duckdb.DuckDBPyConnection, posts: pd.DataFrame, users: pd.DataFrame) -> None:
    """Load DataFrames into DuckDB.
    
    Note: DuckDB resolves the parameter names 'posts' and 'users' 
    in the SQL string to the pandas DataFrames passed into this function.
    """
    con.execute("CREATE OR REPLACE TABLE posts AS SELECT * FROM posts")
    con.execute("CREATE OR REPLACE TABLE users AS SELECT * FROM users")

def transform(con: duckdb.DuckDBPyConnection) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run transformations and create reports."""
    posts_per_user = con.execute("""
        SELECT u.name, u.email, COUNT(p.id) as post_count
        FROM users u
        LEFT JOIN posts p ON u.id = p.userId
        GROUP BY u.id, u.name, u.email
        ORDER BY post_count DESC
    """).fetchdf()
    
    avg_title_length = con.execute("""
        SELECT u.name, 
               ROUND(AVG(LENGTH(p.title)), 1) as avg_title_length
        FROM users u
        JOIN posts p ON u.id = p.userId
        GROUP BY u.id, u.name
        ORDER BY avg_title_length DESC
    """).fetchdf()
    
    return posts_per_user, avg_title_length

def export(df: pd.DataFrame, output_path: str) -> None:
    """Save results to file."""
    Path(output_path).parent.mkdir(exist_ok=True)
    df.to_csv(output_path, index=False)

def main() -> None:
    con = duckdb.connect('etl_demo.duckdb')
    
    print("Extracting...")
    posts, users = extract()
    
    print("Loading...")
    load(con, posts, users)
    
    print("Transforming...")
    posts_per_user, avg_title_length = transform(con)
    
    print("Exporting...")
    export(posts_per_user, 'reports/posts_per_user.csv')
    export(avg_title_length, 'reports/avg_title_length.csv')
    
    print("Done!")
    print(posts_per_user.head())
    print(avg_title_length.head())

if __name__ == "__main__":
    main()
```

## Exercises

These exercises build on the pipeline we just created. Try them out to deepen your understanding.

**Exercise 1: Add a New Data Source**
The JSONPlaceholder API also has a `/comments` endpoint. Fetch it, load it into DuckDB, and write a query that shows the number of comments per post, joined with the post title.

**Exercise 2: Multi-Format Export**
Modify the `export()` function to accept a format parameter (`'csv'`, `'json'`, or `'parquet'`) and write to the appropriate format. Then call it three times to generate all three outputs from a single pipeline run.

**Exercise 3: Add a Transform**
Write a new transformation query that finds the top 3 most active users (the ones with the most posts) and lists each of their post titles. You will need a CTE or subquery (remember [Post 13]({{< relref "subqueries-when-sql-needs-helper-functions" >}}) and [Post 14]({{< relref "ctes-making-your-sql-readable" >}})?).

**Exercise 4: Error Handling**
What happens if the API is down? Wrap the extract step in a try/except block that catches `httpx.HTTPStatusError` and prints a friendly message instead of crashing. Bonus: have it fall back to loading from a local CSV file if the API fails.

**Exercise 5: Build Your Own Pipeline**
Find a different free public API (check out [this list of public APIs](https://github.com/public-apis/public-apis)) and build a pipeline from scratch using the same Extract, Load, Transform, Export pattern. Pick something that interests you (weather data, Pokemon stats, space launches) and write at least two transform queries.

## Next Week

This pipeline works, but there's a security concern hiding in plain sight. What if someone could manipulate the data flowing through our pipeline to run arbitrary SQL? Next week, we will look at parameterized queries and how to prevent SQL injection attacks.
