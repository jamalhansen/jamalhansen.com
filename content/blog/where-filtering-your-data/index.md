---
title: "WHERE: Filtering Your Data"
description: Filter rows with conditions, the SQL equivalent of list comprehension `if` clauses. Covers AND/OR, IN, BETWEEN, LIKE patterns, and NULL handling.
author:
  - Jamal Hansen
date: 2026-03-03
tags:
  - sql
categories:
cover:
  image: "di-bella-coffee-Ko7PFAommGE-unsplash"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Di Bella Coffee"
    username: "dibella"
    photo_id: "shallow-focus-photo-coffee-decanter-Ko7PFAommGE"
draft: false
ShowToc: false
series: "SQL for Python Developers"
weight: 9
---
We have come a long way in the past couple of months, working through the core SQL keywords. So far, we can [`SELECT` columns](https://jamalhansen.com/blog/select-choosing-your-columns), specify [`FROM` where our data lives](https://jamalhansen.com/blog/from-where-your-data-lives), and [`ORDER BY` to sort results](https://jamalhansen.com/blog/order-by-sorting-your-results).

That is quite a lot, and today we are going to unlock the real power of SQL by giving you the ability to filter your results **before** they are returned from the server. 

When you're querying a remote database, this is a huge optimization win; not only will your database send fewer rows of data, but your network and your client will receive less data to sort through. 

To add filtering, we use the `WHERE` keyword. `WHERE` appears after `SELECT` and `FROM`, and it executes second among the keywords we've learned so far.

```
FROM customers        -- 1st: Get the data
WHERE is_premium      -- 2nd: Filter rows
SELECT name, city     -- 3rd: Pick columns
ORDER BY name         -- 4th: Sort results
```

We are adding more keywords, but just remember, `WHERE` filters rows before you see them. It's like Python's `filter()` or list comprehension conditions. 

```python
# Python: filter with list comprehension
[c for c in customers if c['is_premium']]

# Python: filter() function
list(filter(lambda c: c['is_premium'], customers))
```

It will make your queries more efficient and the results exactly what you want to see. 

```sql
SELECT * 
FROM customers
WHERE is_premium = true
```

In both the Python and SQL above, we are limiting the results to only those customers where premium = true.
## The Basics

The simplest way that you can use a `WHERE` clause is to set a column equal to a value. If the value is a string, you will need to surround it with single quotes. Unlike Python, you can't use single and double quotes interchangeably in SQL. Also, it is good to remember that in SQL the equal operator is overloaded, meaning that the single `=` is used for both equality and assignment.
```sql
SELECT name, city FROM customers
WHERE city = 'New York'
```

If you would like to exclude a value, you can use `!=` or `<>`

```sql
SELECT name, city FROM customers
WHERE city != 'New York'
-- Alternate syntax: WHERE city <> 'New York'
```

As you might expect, you can also make comparisons using greater than (`>`) and less than (`<`) operators.
```sql
-- Dates
SELECT name, signup_date FROM customers
WHERE signup_date > '2025-01-01'
-- Works with numbers too!
```
## Combining Conditions
Like Python, SQL provides the ability to specify multiple conditions using `AND` and `OR`

```sql
SELECT name, city FROM customers
WHERE city = 'New York' AND is_premium = true
```

```sql
SELECT name, city FROM customers
WHERE city = 'New York' OR city = 'Los Angeles'
```

### Parentheses for Complex Logic
Parentheses are super important as you build up a `WHERE` clause. Especially if you introduce both `AND` and `OR` logic. Consider the following:
```sql
SELECT name, city, is_premium FROM customers
WHERE is_premium = true 
  AND city = 'New York' 
  OR city = 'Los Angeles'
```

Do you get the results you expect with that query? 

Are the customers from Los Angeles all premium members?

What about this one?
```sql
SELECT name, city, is_premium FROM customers
WHERE is_premium = true 
  AND (city = 'New York' 
		  OR city = 'Los Angeles'
	  )
```

Without parentheses, you might get unexpected results. When in doubt, add them. There have been times that I was sure that I didn't need them that I added them anyway, just for clarity.
## Useful Operators

Here are a few more useful operators that are helpful in a `WHERE` clause. 

### IN: Match Any in a List
Sometimes you want to specify that a column can be any one of a list of values. For this you can use the `IN` keyword with a set of values surrounded by parentheses (note that Python uses square brackets for lists, but SQL uses parentheses here):

```sql
SELECT name, city FROM customers
WHERE city IN ('New York', 'Los Angeles', 'Chicago')
```

The Python equivalent for this would also be the keyword `in`

```python
[c for c in customers if c['city'] in ['New York', 'Los Angeles', 'Chicago']]
```

### BETWEEN: Range of Values
Alternatively, you might want to return a range of values. The `BETWEEN` keyword is very helpful when working with a range of dates or numbers. 
```sql
SELECT name, signup_date FROM customers
WHERE signup_date BETWEEN '2025-01-01' AND '2025-06-30'
```
Just remember that the results will include the beginning and end values.
### LIKE: Pattern Matching

So far, we have talked about matching based on equivalence, which forces the values to be the same. SQL offers partial matching, which can be very helpful. 

There are two things to know about partial or pattern matching with SQL. The first is that if you want to match using patterns, you must use the `LIKE` keyword rather than `=`

The second is that you need to use a wildcard character to say that you would like to return any value for that part of the string. 
```sql
-- Emails ending in gmail.com
SELECT name, email FROM customers
WHERE email LIKE '%@gmail.com'

-- Names starting with 'J'
SELECT name FROM customers
WHERE name LIKE 'J%'
```

There are multiple wildcard characters. Most of the time, you will use `%`, which matches any sequence of characters (including an empty string). Alternatively, you might want to use `_`, which represents a single character.
### IS NULL / IS NOT NULL

To this point, we haven't discussed the `NULL` keyword. It is a very important concept; in fact, we will dedicate an entire post to `NULL` in a few weeks. It represents the lack of a value, sort of like `None` in Python. 

```sql
-- Find rows with missing emails
SELECT name FROM customers
WHERE email IS NULL

-- Find rows that have emails
SELECT name, email FROM customers
WHERE email IS NOT NULL
```

I'm bringing this up now because there is a special syntax to find `NULL` values in a `WHERE` clause. Saying that a column `= NULL` doesn't work. To get `NULL` values, you must use `IS NULL` syntax.

We have covered a lot this week with the `WHERE` clause. You can now filter to exact values, ranges, patterns, and missing data. But what if you want to answer questions like "how many customers per city?" That requires grouping and counting. Next week, we will introduce the `GROUP BY` keyword that allows us to aggregate data.
