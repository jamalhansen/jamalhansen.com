import duckdb
import pandas as pd

# Standard customers dataset used in Python/SQL comparison blocks
customers = [
    {"id": 1, "name": "Alice", "email": "alice@gmail.com", "city": "Denver", "is_premium": True, "signup_date": "2024-01-15"},
    {"id": 2, "name": "Bob", "email": "bob@yahoo.com", "city": "Austin", "is_premium": False, "signup_date": "2024-02-20"},
    {"id": 3, "name": "Charlie", "email": "charlie@gmail.com", "city": "Denver", "is_premium": True, "signup_date": "2024-03-05"},
    {"id": 4, "name": "David", "email": "david@outlook.com", "city": "Seattle", "is_premium": False, "signup_date": "2024-01-22"},
    {"id": 5, "name": "Eve", "email": "eve@gmail.com", "city": "Austin", "is_premium": True, "signup_date": "2024-04-10"},
]

# Standard orders dataset
orders = [
    {"id": 1, "customer_id": 1, "product": "Widget", "amount": 50.0, "order_date": "2024-05-01"},
    {"id": 2, "customer_id": 2, "product": "Gizmo", "amount": 25.0, "order_date": "2024-05-02"},
    {"id": 3, "customer_id": 1, "product": "Doodad", "amount": 75.0, "order_date": "2024-05-03"},
    {"id": 4, "customer_id": 4, "product": "Widget", "amount": 50.0, "order_date": "2024-05-04"},
]

# Provide them as DataFrames as well (common in posts)
customers_df = pd.DataFrame(customers)
orders_df = pd.DataFrame(orders)

# Convert signup_date and order_date to proper datetime types for DuckDB
customers_df['signup_date'] = pd.to_datetime(customers_df['signup_date'])
orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])

# Inject them into DuckDB if we have a connection
try:
    if 'conn' in globals():
        conn.execute("CREATE TABLE IF NOT EXISTS customers AS SELECT * FROM customers_df")
        conn.execute("CREATE TABLE IF NOT EXISTS orders AS SELECT * FROM orders_df")
except Exception:
    pass
