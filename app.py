import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        pragma = '''PRAGMA foreign_keys = ON'''
        cursor.execute(pragma)
        print(f"Connected to {db_file}, sqlite version: {sqlite3.sqlite_version}")
        return conn
    except Error as e:
            print(e)

def create_clients_table(conn):
    cursor = conn.cursor()
    sql_create_clients_table = '''CREATE TABLE IF NOT EXISTS clients 
    (id INTEGER PRIMARY KEY, 
    name TEXT NOT NULL, 
    second_name TEXT NOT NULL, 
    address TEXT NOT NULL)'''
    cursor.execute(sql_create_clients_table)
    conn.commit()

def create_orders_table(conn):
    cursor = conn.cursor()
    sql_create_orders_table = '''CREATE TABLE IF NOT EXISTS orders 
    (id INTEGER PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    product_description TEXT NOT NULL,
    product_price FLOAT NOT NULL,
    order_date TEXT NOT NULL,
    payment_status TEXT NOT NULL)'''
    cursor.execute(sql_create_orders_table)
    conn.commit()




if __name__ == '__main__':
   conn = create_connection(r"database.db")
   create_clients_table(conn)
   create_orders_table(conn)
   cursor = conn.cursor()
   sql_insert_client = '''
   INSERT INTO clients (name, second_name, address)
   VALUES (?, ?, ?)
   '''
   name = 'Brad'
   second_name = 'Pitt'
   address = 'Miami 234'

   values_client = (name, second_name, address)
   cursor.execute(sql_insert_client, values_client)
   conn.commit()

   sql_insert_order = '''
   INSERT INTO orders (client_id, product_name, quantity, product_description, product_price, order_date, payment_status)
   VALUES (?, ?, ?, ?, ?, ?, ?)
   '''

   client_id = 2
   product_name = 'beer'
   quantity = 1
   product_description = 'alcohol'
   product_price = 2.0
   order_date = '2023-10-01'
   payment_status = 'finished'

   values_order = (client_id, product_name, quantity, product_description, product_price, order_date,
                   payment_status)
   cursor.execute(sql_insert_order, values_order)
   conn.commit()
   conn.close()

