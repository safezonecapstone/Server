from sqlalchemy import create_engine, engine, Table, MetaData
from os import getenv

# Generate Google Cloud SQL connection pool
db_user = getenv('DB_USER')
db_pass = getenv('DB_PASS')
db_name = getenv('DB_NAME')
sql_socket_url = getenv('DB_SOCKET_URL')

db = create_engine(
    engine.url.URL(
        drivername='postgres+pg8000',
        username=db_user,
        password=db_pass,
        database=db_name,
        query={
          'unix_sock': sql_socket_url
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
