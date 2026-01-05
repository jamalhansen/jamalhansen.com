---
title: I know Python; Why learn SQL
summary: Learning SQL will make you a better Python developer, even if you already use pandas and ORMs. The first in a series of posts that will walk you through the fundamentals using DuckDB and Python.
author:
  - Jamal Hansen
date: 2026-01-05
lastmod: ""
tags:
  - "#sql"
  - "#duckdb"
  - "#python"
categories:
featureimage: anna-yablonskaya-cpy88m2PnBM-unsplash.jpg
cardimage: why-learn-sql-thumb.png
draft: true
toc: false
series: "SQL for Python Developers"
canonical_url: https://jamalhansen.com/blog/i-know-python-why-learn-sql
slug: i-know-python-why-learn-sql
layout: post

---
{{< unsplash-credit name="Anna Yablonskaya" username="invborder" photo-id="a-foggy-train-station-with-a-train-on-the-tracks-cpy88m2PnBM" >}}

I learned SQL very early in my career. At the time, I didn't understand why, and for the first month or so, it didn't make sense to me. The syntax didn't resemble any language I had seen before, and it employed concepts with which I was unfamiliar. This all made SQL seem scary, and oddly enough, SQL hasn't changed much in the past 40 years, which makes it even more of an oddity. 

The problem wasn't the SQL; it was how I was thinking. I had some experience with coding, but only in a procedural style, telling the computer to perform a series of steps in order. My aha moment was when I realized that SQL doesn't do this. Instead, a SQL query describes the data that you would like, and it returns that dataset. Making this mind shift turned SQL into a beautiful and functional language that is relatively simple to learn. 

SQL is the language of data, and over the past 40 years, data has become more prevalent and more important. If you work with data, learning SQL will help you. This is true even if you already know and use another programming language like Python with good data management libraries. Python has great data support with SQL Alchemy, Pandas, and other great libraries. Learning SQL won't replace them, but it will help you use them more effectively. When you understand how SQL thinks, you'll write better pandas queries, ask smarter questions of your ORM, and know when to push work to the database instead of pulling everything into memory.

In this series, I'll walk you through the steps to level up your SQL skills. We will use Python along the way to keep things practical. Our first step will be to set up a database. This is the biggest hurdle for beginners: you need a database to practice, but setting one up feels intimidating before you know what you're doing. For this series, we will use a modern, local, and user-friendly database called DuckDB, which is simple to get started with. 

Next, we will dig into querying data. We will learn about keywords such as SELECT, FROM, WHERE, and GROUP BY, and how they can be used to shape your results.

Finally, we will tackle some more complex topics, like when it's useful to use SQL over an ORM or Pandas, and why you might consider it. 

If you are a Python developer, you work with data. Follow along, and I'll see you next week to set up DuckDB.
