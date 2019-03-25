from sqlalchemy import create_engine, engine, Table, MetaData
from os import getenv

# Generate Google Cloud SQL connection pool

db = create_engine(
    engine.url.URL(
        drivername='postgres+pg8000',
        username=getenv('DB_USER'),
        password=getenv('DB_PASS'),
        database=getenv('DB_NAME'),
        query={
          'unix_sock': getenv('DB_SOCKET_URL')
        }
    ),
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

metadata = MetaData(bind=db)
crimes = Table('crime_info', metadata, autoload=True)
categories = Table('crime_categories', metadata, autoload=True)
stations = Table('stations', metadata, autoload=True)
