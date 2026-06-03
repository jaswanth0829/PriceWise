import sqlite3

conn = sqlite3.connect(
    "database.db"
)

cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    email TEXT UNIQUE,

    password TEXT
)
""")

# PRODUCTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    name TEXT,

    price REAL,

    url TEXT,

    target_price REAL
)
""")

# PRICE HISTORY TABLE
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

print(
    "Database created successfully"
)