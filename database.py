import psycopg2
from psycopg2 import pool
from config import DB_CONFIG

try:
    db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **DB_CONFIG)
    if db_pool:
        print("postgresql connection pool created successfully")
except Exception as e:
    print(f"error creating connection pool: {e}")

def get_db_connection():
    return db_pool.getconn()

def return_db_connection(conn):
    db_pool.putconn(conn)
