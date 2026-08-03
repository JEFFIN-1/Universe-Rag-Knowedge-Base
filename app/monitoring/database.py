import psycopg

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "rag_monitoring",
    "user": "raguser",
    "password": "ragpassword",
}


def get_connection():
    return psycopg.connect(**DB_CONFIG)