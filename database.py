import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

# Products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    price REAL,

    url TEXT,

    target_price REAL
)
""")

# Price history table
cursor.execute("""
CREATE TABLE IF NOT EXISTS price_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    product_id INTEGER,

    price REAL,

    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

conn.close()

print("Database created successfully")