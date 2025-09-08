import psycopg2
from psycopg2 import pool
from app.core.config import get_settings

settings = get_settings()

try:
    db_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=20,
        user=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name
    )
except Exception as e:
    raise RuntimeError(f"Error setting up connection pool: {e}")

def get_db_connection():
    conn = db_pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)

def init_db():
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    role VARCHAR(50),
                    batting_style VARCHAR(50),
                    bowling_style VARCHAR(50),
                    matches INTEGER,
                    runs INTEGER,
                    average FLOAT,
                    strike_rate FLOAT,
                    image_url VARCHAR(200)
                )
            """)
            conn.commit()
    except Exception as e:
        raise RuntimeError(f"Error initializing database: {e}")
    finally:
        db_pool.putconn(conn)
        