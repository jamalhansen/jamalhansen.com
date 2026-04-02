---
slug: congratulations-what-you-can-do-now
title: Congratulations! What You Can Do Now
description: Celebrate your new skills with take-home challenges and resources for continued learning. You think in sets now.
author:
  - Jamal Hansen
date: 2026-06-22
tags:
  - sql
categories:
cover:
  image: "rona-lao-vrkDu_tpJJI-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Rona Lao"
    username: "ronalao"
    photo_id: "person-sitting-on-rock-formation-during-golden-hour-vrkDu_tpJJI"
draft: false
ShowToc: false
series: "SQL for Python Developers"
unsplash_user: ronalao
---

Twenty-four weeks ago, I started this series with a confession: SQL seemed scary to me when I first learned it. The syntax didn't look like any language I had seen before. The concepts felt unfamiliar. I was trying to tell SQL what steps to perform, and it kept not working.

The problem wasn't the SQL. It was how I was thinking.

If you've followed along to this point, you've made that same shift. You think in sets now. You describe the result you want instead of writing loops to build it row by row. That mental model is the real skill, and it's yours to keep.

## What You Can Do Now

Let's take stock of where you are. This isn't abstract. These are concrete things you can do today that you couldn't do 24 weeks ago.

**You can query any database.** You know [SELECT](https://jamalhansen.com/blog/select-choosing-your-columns), [FROM](https://jamalhansen.com/blog/from-where-your-data-lives), [WHERE](https://jamalhansen.com/blog/where-filtering-your-data), [ORDER BY](https://jamalhansen.com/blog/order-by-sorting-your-results), [GROUP BY](https://jamalhansen.com/blog/group-by-aggregating-your-data), and [HAVING](https://jamalhansen.com/blog/having-filtering-grouped-results). You understand how they execute (FROM first, SELECT near the end) and why that order matters. You can connect to DuckDB, SQLite, or PostgreSQL and start writing queries immediately.

**You think in sets.** You understand the difference between [declarative and procedural code](https://jamalhansen.com/blog/sql-thinks-in-sets-not-loops). When someone asks "how many customers per city?", your instinct is GROUP BY, not a for loop. That shift changes how you approach every data problem.

**You can combine data across tables.** [JOINs](https://jamalhansen.com/blog/joins-explained-for-python-developers), [subqueries](https://jamalhansen.com/blog/subqueries-when-sql-needs-helper-functions), and [CTEs](https://jamalhansen.com/blog/ctes-making-your-sql-readable) let you answer questions that span multiple tables. You know when INNER JOIN drops rows and when LEFT JOIN preserves them. You can write CTEs that read top-to-bottom instead of nested subqueries that read inside-out.

**You can do real analytics.** [Window functions](https://jamalhansen.com/blog/window-functions-the-feature-python-developers-miss-most) give you running totals, rankings, and row-to-row comparisons without collapsing your data. [CASE statements, date functions, and string functions](https://jamalhansen.com/blog/advanced-topics-sampler) let you categorize, slice by time period, and clean data on the fly.

**You can build and modify databases.** [CREATE TABLE](https://jamalhansen.com/blog/creating-tables-ddl-for-python-devs), INSERT, [UPDATE, DELETE](https://jamalhansen.com/blog/modifying-data-safely). You know the [SELECT-first workflow](https://jamalhansen.com/blog/modifying-data-safely) that prevents disasters. You understand transactions and why ROLLBACK exists.

**You can build real pipelines.** [Extract data from an API, load it into DuckDB, transform it with SQL, and export the results.](https://jamalhansen.com/blog/python-duckdb-real-etl-patterns) That's a production pattern, not a tutorial exercise.

**You write safe, testable SQL.** [Parameterized queries](https://jamalhansen.com/blog/parameterized-queries-and-security) protect against injection. [Pytest fixtures with in-memory databases](https://jamalhansen.com/blog/testing-sql-code) let you test your queries the same way you test your Python code. And you know [when to reach for an ORM and when to write raw SQL](https://jamalhansen.com/blog/orm-vs-raw-sql-decision-framework).

That's a complete toolkit. Not a beginner's toolkit. A working one.

## Take-Home Challenges

Reading is one thing. Building is where the learning sticks. Here are five projects to try on your own. Each one uses skills from across the series.

If you set up DuckDB back in [Post 2](https://jamalhansen.com/blog/run-your-first-sql-query-in-under-5-minutes), you already have everything you need to start.

### Challenge 1: Personal Finance Tracker

Create tables for accounts, transactions, and categories. If your bank lets you export a CSV, import your real data. Write queries for monthly spending by category, running account balance (window functions), and spending trends over time. This project uses [CREATE TABLE](https://jamalhansen.com/blog/creating-tables-ddl-for-python-devs), INSERT, [GROUP BY](https://jamalhansen.com/blog/group-by-aggregating-your-data), [window functions](https://jamalhansen.com/blog/window-functions-the-feature-python-developers-miss-most), and [date functions](https://jamalhansen.com/blog/advanced-topics-sampler).

### Challenge 2: Reading List Analyzer

Build a table to track books: title, author, genre, date read, and your rating. Seed it with [Faker](https://jamalhansen.com/blog/generate-practice-data-with-faker) or use your actual reading history. Write queries to find your most-read genres, average rating by year, longest gaps between books, and how your reading habits have changed over time. This project uses dates, aggregations, [CASE statements](https://jamalhansen.com/blog/advanced-topics-sampler), and window functions.

### Challenge 3: API Data Pipeline

Pick a free API (weather, sports scores, stock prices, or anything that interests you) and build the full ELT pipeline from [Post 20](https://jamalhansen.com/blog/python-duckdb-real-etl-patterns). Fetch the data, load it into DuckDB, transform it with [CTEs](https://jamalhansen.com/blog/ctes-making-your-sql-readable) and [JOINs](https://jamalhansen.com/blog/joins-explained-for-python-developers), and export a summary. Bonus: schedule it to run daily and watch your dataset grow.

### Challenge 4: Analyze a Public Dataset

Find a dataset on [Kaggle](https://www.kaggle.com/datasets), [data.gov](https://data.gov), or a similar source. Load it into DuckDB and answer five interesting questions using SQL. Write up your findings. This is the closest exercise to real data work: start with messy data, figure out what's interesting, and tell a story with queries.

### Challenge 5: Teach Someone Else

This is the most effective way to solidify what you've learned. Walk a colleague through [Post 1](https://jamalhansen.com/blog/i-know-python-why-learn-sql) through [Post 5](https://jamalhansen.com/blog/sql-thinks-in-sets-not-loops). Answer their questions. You'll discover which concepts you understand deeply and which ones need another look. Teaching is the best test of understanding.

## Where to Go Next

You have a strong foundation. Here are some paths forward depending on where your interests take you.

### Deepen Your SQL

"SQL for Data Scientists" by Renee Teate is a great next-level book. The PostgreSQL documentation is the gold standard for SQL reference. [SQLBolt](https://sqlbolt.com/) offers interactive exercises for additional practice. And if you want interview prep, [LeetCode's SQL problems](https://leetcode.com/problemset/database/) are a solid way to sharpen your skills under pressure.

### Learn Related Tools

dbt (data build tool) is widely used for SQL-first data transformations in production. Apache Superset and Metabase let you build dashboards powered by SQL queries. Great Expectations handles data quality testing. These tools all assume you know SQL, and now you do.

### Apply It at Work

The fastest way to cement these skills is to use them on a problem you already care about. Find a pandas workflow and rewrite the heavy lifting in SQL. Identify a slow ORM query and [optimize it with EXPLAIN](https://jamalhansen.com/blog/optimizing-queries-explain-for-python-developers). Build a reporting pipeline with DuckDB. Propose SQL-based analytics to your team. Real problems are where the learning compounds.

### Join the Community

You have something most pure SQL developers don't: a Python background that lets you bridge both worlds. Follow SQL and data engineering creators on LinkedIn and Twitter. Join data engineering communities on Discord or Slack. Share what you build. Answer SQL questions on Stack Overflow. The data community is welcoming, and your dual perspective is an asset.

## Full Circle

In [Post 1](https://jamalhansen.com/blog/i-know-python-why-learn-sql), I wrote: "The problem wasn't the SQL; it was how I was thinking." In [Post 5](https://jamalhansen.com/blog/sql-thinks-in-sets-not-loops), we explored that idea further and learned to think in sets instead of loops.

You've made that shift. You see data differently now. When you look at a problem, you think about what the result should look like, not what steps to take to get there. That's the real transformation, and it makes you a better Python developer too.

The goal of this series was never to make you a DBA or a database expert. It was to add SQL to your Python toolkit. To know when it's the right tool and to use it with confidence.

You've done that. Twenty-four weeks of showing up, reading, and practicing. That's real commitment, and it paid off.

## Thank You

I want to end with a genuine thank you. Writing this series has been one of the most rewarding projects I've worked on. Your engagement, your questions, and your willingness to follow along week after week shaped the series into something better than I could have planned alone.

If something in this series helped you, I'd love to hear about it. Reply to the newsletter, leave a comment, or reach out on [LinkedIn](https://www.linkedin.com/in/jamalhansen/). Tell me which post clicked for you, which challenge you're going to try first, or what topic you'd like to see next.

And if you know a Python developer who could benefit from this series, send them to [Post 1](https://jamalhansen.com/blog/i-know-python-why-learn-sql). Everything is there, start to finish, for free.

This series is complete, but the newsletter isn't going anywhere. I have more to write about, and I'm excited about what comes next. Stay tuned.

Thank you for reading. Now go build something.

-Jamal