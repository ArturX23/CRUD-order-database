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
    sql_create_clients_table = '''CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY, 
        name TEXT NOT NULL, 
        second_name TEXT NOT NULL, 
        address TEXT NOT NULL
    )'''
    cursor.execute(sql_create_clients_table)
    conn.commit()

def create_orders_table(conn):
    cursor = conn.cursor()
    sql_create_orders_table = '''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id),
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        product_description TEXT NOT NULL,
        product_price FLOAT NOT NULL,
        order_date TEXT NOT NULL,
        payment_status TEXT NOT NULL
    )'''
    cursor.execute(sql_create_orders_table)
    conn.commit()

def add_client(conn, client_data):
    try:
        client_details = (client_data['name'],
                          client_data['second_name'],
                          client_data['address'])
        cursor = conn.cursor()
        sql_insert_client = '''INSERT INTO clients (
            name, 
            second_name, 
            address
        ) VALUES (?, ?, ?)'''
        cursor.execute(sql_insert_client, client_details)
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)

def add_order(conn, order_data):
    try:
        order_details = (order_data['client_id'],
                         order_data['product_name'],
                         order_data['quantity'],
                         order_data['product_description'],
                         order_data['product_price'],
                         order_data['order_date'],
                         order_data['payment_status'])
        cursor = conn.cursor()
        sql_insert_order = '''INSERT INTO orders (
        client_id, 
        product_name, 
        quantity, 
        product_description, 
        product_price, 
        order_date, 
        payment_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(sql_insert_order, order_details)
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)

def get_orders_by_client(conn, client_id):
    try:
        cursor = conn.cursor()
        sql_select_orders_by_client = '''SELECT * FROM orders WHERE client_id = ?'''
        cursor.execute(sql_select_orders_by_client, (client_id,))
        results = cursor.fetchall()
        return results
    except Error as e:
        print(e)

def update_payment_status(conn, order_id, updated_payment_status):
    try:
        cursor = conn.cursor()
        sql_update_payment_status = '''
        UPDATE orders 
        SET payment_status = ? 
        WHERE id = ?
        '''
        cursor.execute(sql_update_payment_status, (updated_payment_status, order_id))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        print(e)

if __name__ == '__main__':
   conn = create_connection(r"database.db")
   create_clients_table(conn)
   create_orders_table(conn)
   # 3️⃣ dane klienta
   client_data = {
       "name": "Brad",
       "second_name": "Pitt",
       "address": "Miami 234"
   }

   # 4️⃣ dodanie klienta i pobranie jego ID
   client_id = add_client(conn, client_data)

   # 5️⃣ dane zamówienia z ID klienta
   order_data = {
       "client_id": client_id,
       "product_name": "sugar",
       "quantity": 1,
       "product_description": "alcohol",
       "product_price": 2.0,
       "order_date": "2023-10-01",
       "payment_status": "finished"
   }

   # 6️⃣ dodanie zamówienia
   order_id = add_order(conn, order_data)

   # 7️⃣ zamknięcie połączenia

   result = update_payment_status(conn, 5, "paid")

   if result == 50:
       print("Status zamówienia został zaktualizowany")
   else:
       print("Nie znaleziono zamówienia o podanym ID")

   conn.close()

