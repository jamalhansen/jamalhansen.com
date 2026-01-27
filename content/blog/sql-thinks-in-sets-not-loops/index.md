---
title: SQL Thinks in Sets, Not Loops
description: "The mental model shift that makes SQL click: SQL is declarative (describe what you want) rather than procedural (step-by-step loops). Once you think in sets instead of rows, the keywords become intuitive."
date: 2026-02-02
tags: ["sql"]
categories: []
cover:
    image: dimitry-b-S9T2A1dPRiY-unsplash.jpg
    alt: "SQL Thinks in Sets, Not Loops"
    relative: true
    caption: ""
    credit:
        name: "Dimitry B"
        username: "dimitry_b"
        photo_id: "a-person-is-sprinkling-seeds-on-a-wooden-table-S9T2A1dPRiY"
draft: false
ShowToc: false
TocOpen: false
series: ["SQL for Python Developers"]
weight: 5
---

Remember [back when we started](https://jamalhansen.com/blog/i-know-python-why-learn-sql), I mentioned SQL was difficult because of how I was thinking? I was asking it to perform steps to return data. This didn't work because SQL uses a declarative syntax that describes the final result. Until I realized this, SQL felt hard. Let's explore this concept further.

## Working with lists and loops

When you work with lists in Python, one of the first tools you reach for is the `for` loop. The for loop is great because it lets you take every item in the list and apply some logic to it, one at a time. It might look something like this.

```python
# Step-by-step instructions
results = []
for customer in customers:
    if customer['is_premium']:
        results.append(customer['name'])
```

This is how I might handle logic for lists in Python. It's fine. It works. It's readable. 

But when we look at the work that it's doing, it is really just filtering data into another list. Python has a syntax that is great for that: List comprehensions. These are somewhat like a rearranged for loop, but they are also taking a step towards the declarative syntax that SQL uses. 

The code is compact and breaks down into three parts: `c['name'] for c` selects and transforms, `in customers` specifies the source, and `if c['is_premium']` filters.

```python
# Python: More declarative (list comprehension)
premium_names = [c['name'] for c in customers if c['is_premium']]
```

In a lot of ways, this is written as it would be in SQL. The steps that you would take are omitted. There is no looping visible. Just the same three components: `SELECT name` selects and transforms, `FROM customers` specifies the source, and `WHERE is_premium = true` filters.

```sql
-- Describe the result you want
SELECT name FROM customers WHERE is_premium = true
```

Same logic, same structure. If you can read a list comprehension, you can read SQL.

## A Spreadsheet Analogy

Let's look at this another way to help clarify the difference. This time, let's consider a spreadsheet. If we had a spreadsheet that lists 1,000 people and we needed to see only the people who live in Texas, there are a few ways we could do this.

### The slow way
You might look at each row in the spreadsheet, starting from the top, and when you find someone who lives in Texas, copy the row to another sheet. 

### The clever way
You might be a bit more advanced and sort the State column on the spreadsheet first, and then scroll down to find Texas alphabetically, select those rows, copy them, and paste them into a new sheet. This approach has some advantages because it's more efficient. You don't have to look at every row in order, but you are still performing steps in order to produce the final result. 

### The SQL way 
Go to the spreadsheet, filter the state to Texas. No multiple steps, just describing the end result, and it's done.

## Why does SQL work like this?

SQL is designed to work with data of all sizes. It can handle a simple database like ours that has one table with 500 rows. It can also handle databases with hundreds of tables and billions of rows. 

When working with large amounts of data, it is easier to think in terms of describing sets of data rather than the steps that it takes to make them. It lets the database optimize for faster results, because the database can choose the fastest path to your result.

Writing queries in this way is also cleaner and more readable, because ultimately, a SQL developer will write the code and need to read it later on. If there is one thing that I have learned, it is that I am often the SQL developer who will need to read my code in the future. I want to make things easier for my future self. 

Finally, the syntax stays the same regardless of the amount of data present. If I describe a dataset, it will be described in the same way whether I have 10 rows of data or ten thousand.

## Conclusion

That's the mental shift that helps SQL make sense. When we start writing SQL next week, remember to think of it this way, and it will be easier. 

Next time, we will look a bit closer at the FROM clause. It is where every query begins.