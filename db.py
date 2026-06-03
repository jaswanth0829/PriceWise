import sqlite3

from config import DATABASE_NAME

def get_connection():

    conn = sqlite3.connect(
        DATABASE_NAME
    )

    return conn