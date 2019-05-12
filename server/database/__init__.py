from sqlalchemy import create_engine, engine
from os import getenv
from sqlalchemy import create_engine, engine

# Generate Google Cloud SQL connection pool

URL = {
    'drivername': 'postgresql+pg8000',
    'username': getenv('DB_USER'),
    'password': getenv('DB_PASS'),
    'database': getenv('DB_NAME'),
    'query': {
        'unix_sock': getenv('DB_SOCKET_URL')
    }
}

db = create_engine(
    engine.url.URL(**URL),
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)