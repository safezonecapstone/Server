from sqlalchemy import create_engine, engine, Table, MetaData
from os import getenv

# Generate Google Cloud SQL connection pool
db_user = getenv('DB_USER')
db_pass = getenv('DB_PASS')
db_name = getenv('DB_NAME')
cloud_sql_instance = getenv('DB_CONNECTION_NAME')

db = create_engine(
    engine.url.URL(
        drivername='postgres+pg8000',
        username=db_user,
        password=db_pass,
        database=db_name,
        query={
          'unix_sock': '/cloudsql/{}/.s.PGSQL.5432'.format(cloud_sql_instance)
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
