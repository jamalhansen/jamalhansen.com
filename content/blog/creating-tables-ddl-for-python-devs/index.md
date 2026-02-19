---
title: "Creating Tables: DDL for Python Devs"
description: Map Python types to SQL types. Learn CREATE TABLE with primary keys, foreign keys, and constraints like NOT NULL and DEFAULT.
author:
  - Jamal Hansen
date: 2026-04-27
tags:
  - sql
categories:
cover:
  image: "ryno-marais-p5JcD-_13ek-unsplash.jpg"
  alt: ""
  caption: ""
  relative: true
  credit:
    name: "Ryno Marais"
    username: "ryno_marais"
    photo_id: "person-in-white-shirt-holding-brown-wooden-table-p5JcD-_13ek"
draft: false
ShowToc: false
series: "SQL for Python Developers"
weight: 17
---
So far, we have spent our time learning how to query data. For most of us, this might be as much SQL as we will ever use. 

There is a whole other side to SQL used to design and define tables that are optimized to store and return data quickly. 

Even if you only plan to query someone else's data, it is still helpful to get an understanding of SQL's Data Definition Language (DDL) because it will help you to understand how the data is stored, and how to write better queries.

## Data Types

The first building block to learn about SQL or any language is typically the data types. So far we have been able to largely ignore these, but now that we are designing tables let's spend a few minutes understanding data types in SQL.

Let's take a look at how SQL's data types compare to those in Python.

| Python              | SQL (DuckDB)    | Notes                                                                                                                                                        |
| ------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `int`               | INTEGER, BIGINT | BIGINT holds larger numbers, but INT is enough for most needs.                                                                                               |
| `float`             | DOUBLE, DECIMAL | Use DECIMAL for money                                                                                                                                        |
| `str`               | VARCHAR, TEXT   | Use VARCHAR(n) to limit the maximum length of strings. TEXT is generally used for very large blocks of text and is not as versatile as your standard VARCHAR |
| `bool`              | BOOLEAN         | True and False values                                                                                                                                        |
| `datetime.date`     | DATE            | Dates only                                                                                                                                                   |
| `datetime.datetime` | TIMESTAMP       | Date + time                                                                                                                                                  |
| `list`, `dict`      | JSON            | DuckDB supports JSON, but not all databases do.                                                                                                              |
There may be additional types that your particular database supports. It's common to have a BLOB type for binary objects, which can be images or other large binary objects. 

SQL is a strongly typed language, and the database vendor you use will determine how explicit you will need to be with your type conversions. 

On the one hand, SQL Server is very forgiving and will do its best to implicitly convert types for you. If it sees a string that looks like a date ('2026-02-18') and you are using it like a date, it will go ahead and convert it to a date for you

Oracle, on the other hand, takes the opposite approach. It will notice that you are playing fast and loose with your data types, and it will yell at you, and you will need to explicitly convert the data types. 

Like most things, there are pros and cons to each approach. I mention it because it's important to help decipher the messages or errors that you receive when you try to use the database. Today, all we need to worry about is DuckDB, which is generally very friendly. 

## Basic CREATE TABLE

Now that we have a basic understanding of SQL types, let's use them to define a table. This statement will create a products table with 5 columns. 

The VARCHAR(100) means that the `name` can hold up to 100 characters of text.

DECIMALs are not a floating-point type, they have a defined precision. The definition `DECIMAL(10,2)` means that the column will hold a total of 10 digits and 2 of them are after the decimal point. The largest number this column will hold is 99999999.99.
```sql
CREATE TABLE products (
    id INTEGER,
    name VARCHAR(100),
    price DECIMAL(10, 2),
    in_stock BOOLEAN,
    created_at TIMESTAMP
)
```

In Python, this would equate to something like this:
```python
@dataclass
class Product:
    id: int
    name: str          # max 100 chars
    price: Decimal     # 10 digits, 2 decimal places
    in_stock: bool
    created_at: datetime
```

## Primary Keys
Previously, [we talked about how joins are the superpower of relational databases](https://jamalhansen.com/blog/joins-explained-for-python-developers). Properly defining primary keys on your tables is the secret to unlocking that power. 
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,  -- Unique identifier
    name VARCHAR(100),
    price DECIMAL(10, 2)
)
```

A primary key is a column that is:
- unique
- not null
- identifies a row

Also, it is usually a number, though it doesn't have to be. 

In Python, you might do something similar by creating a dict where each key is a unique number, and each value is a data record.
```python
# Like using id as dict key
products = {
    1: {'name': 'Widget', 'price': 9.99},
    2: {'name': 'Gadget', 'price': 19.99}
}
```

Primary keys are nice because, in practice, they allow you to summarize an entire row of data as a number. If you talk about a record in the customers table with a primary key of 42, you are referencing one specific record, and it is all you need to know. The primary key is like a pointer to that record. 

Primary keys on their own don't unlock the relational superpower. To do that, we also need to talk about the other half of the relation, the foreign key.

## Foreign Keys

A foreign key is simply a column in a table that references, or points to, a primary key of a record in another table. 

In this example, we see a table with 4 columns, and 3 of them are keys. 

The first, `id` is the primary key of the table, and we've learned that it uniquely identifies a row in the `orders` table. Because it is a primary key, we know that it is unique and never null.

The other two keys are foreign keys, which means that they contain a number that is a pointer to a record in another table. 

The `customer_id` column points to a customer in the `customers` table

The `product_id` column points to a product in the products table.

So if you think about the following table, each record will contain an order. That order is associated with one customer and one product, and it also has a quantity. 

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),  -- Foreign key
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER
)
```

One more thing about foreign keys. They must exist in the referenced table, otherwise the record is invalid. 

You might be asking, well, if the foreign key is just an integer that contains the primary key in the other table, can I just store that in a normal column? 

The answer is, you could, but declaring the column as a foreign key tells the database that you want to use it as one. The database will help you ensure that the value in the column remains valid. This is also known as enforcing referential integrity. 

Let's take a quick look at how this might work in Python.
```python
# customer_id must be a valid key in the customers dict
order = {'customer_id': 42, ...}
assert order['customer_id'] in customers
```

## Constraints
Databases can become messy places if you don't set up some rules. Those rules are called constraints. If you try to do something to violate a constraint, like set a `NOT NULL` column to `NULL`, the database will stop you.

### NOT NULL
Here is how you would make a field required in a database by using a `NOT NULL` constraint.

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR NOT NULL,  -- Required field
    nickname VARCHAR         -- Optional (NULL allowed)
)
```

### DEFAULT Values
Sometimes, you might want to ensure that a column is never null, but you don't always have a value for it. Think of an order. If you just create an order, you probably want to set it to a new status, but you don't always want to have to set it to new. You also want to keep people from setting it to pending, created, or `NULL`. 

This is where default values come in. If an insert statement would make the column `NULL`, the database will set it to the default value instead.
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    status VARCHAR DEFAULT 'New',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### UNIQUE
If you want to ensure that a value appears in a column only once, you can use a `UNIQUE` constraint. 
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL  -- No duplicate emails
)
```
The above example would only allow the email address `example@example.com` to be used for one user. 

## Practical Example: Full Schema
Now let's look at an example set of `CREATE TABLE` statements to create a schema. Here we can see customers, products, and orders tables. The order has foreign keys to the customers and products. 

Note the `IF NOT EXISTS` clause. This is a handy safeguard that prevents an error if the table has already been created. Without it, running the same `CREATE TABLE` twice would fail.

```sql
-- Customers
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    city VARCHAR(100),
    signup_date DATE DEFAULT CURRENT_DATE,
    is_premium BOOLEAN DEFAULT false
);

-- Products
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50)
);

-- Orders (links customers and products)
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER DEFAULT 1,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## DROP and ALTER

SQL also provides a way to delete a table. To do this, you can use the `DROP TABLE` statement. Be careful, there is no `UNDROP` command so the table and all the data in it will be gone. 
```sql
DROP TABLE products;
DROP TABLE IF EXISTS products;  -- No error if missing
```

You can also change the definition of a table if you need to add, remove, or change the definition of a column. 
```sql
-- Add column
ALTER TABLE customers ADD COLUMN phone VARCHAR(20);

-- Drop column
ALTER TABLE customers DROP COLUMN phone;
```

## Try It Yourself

### Challenge 1: Create a Table

Create a `books` table with the following columns: `id` as an INTEGER primary key, `title` as a VARCHAR(200) that cannot be null, `author` as a VARCHAR(100), `published_date` as a DATE, and `page_count` as an INTEGER with a default value of 0. After creating the table, run a quick `SELECT * FROM books` to confirm it exists.

### Challenge 2: Drop and Recreate

Drop your `books` table using `DROP TABLE IF EXISTS`. Then recreate it, but this time add a UNIQUE constraint on `title`. Try inserting two rows with the same title and see what happens. (Hint: `INSERT INTO books (id, title) VALUES (1, 'Dune');` We'll cover INSERT in detail next week.)

## What's Next?

Great! Now you can create tables. But how do you add, update, and delete data safely? Next week, we will learn to INSERT, UPDATE, and DELETE data.