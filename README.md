SQLite Orders Management 🗂️

A simple Python project demonstrating CRUD operations on a SQLite database with clients and orders.

Features

Create clients and orders tables (1:N relationship)

Add, retrieve, update, and delete orders and clients

Parameterized SQL queries (safe from SQL injection)

Returns feedback on updates/deletions

Quick Start
git clone https://github.com/yourusername/sqlite-orders-project.git
cd sqlite-orders-project
python app.py
Example Usage
conn = create_connection("database.db")

# Add a client
client_id = add_client(conn, {"name": "Brad", "second_name": "Pitt", "address": "Miami 234"})

# Add an order
order_id = add_order(conn, {
    "client_id": client_id,
    "product_name": "Beer",
    "quantity": 1,
    "product_description": "Alcohol",
    "product_price": 2.0,
    "order_date": "2023-10-01",
    "payment_status": "finished"
})

# Update payment status
update_payment_status(conn, order_id, "paid")

# Get orders by client
orders = get_orders_by_client(conn, client_id)

# Delete order
delete_order(conn, order_id)

conn.close()
Requirements

Python 3.x

SQLite3 (built into Python standard library)

License

MIT License
