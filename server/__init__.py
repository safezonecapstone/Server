from dotenv import load_dotenv
from os import getenv
import sqlalchemy
from flask import Flask
import logging

# Create App Instance and associate with API
app = Flask(__name__)

logger = logging.getLogger()

# Load Environment Variables
load_dotenv('.flaskenv')
load_dotenv('.env')

# Generate Google Cloud SQL connection pool
db_user = getenv('DB_USER')
db_pass = getenv('DB_PASS')
db_name = getenv('DB_NAME')

db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername='postgres+pg8000',
        username=db_user,
        password=db_pass,
        database=db_name,
        host='127.0.0.1',
        port='5234'
    ),
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)


# TRAIN_LINE
# Possible values:
# ----

# CRIME_NAME
# Possible values:
# ----

# timeSpan
# Possible Values:
# 'YEAR' - Year To Date
# 'MONT' - Last 28 Days
# 'WEEK' - Week To Date


@app.route('/')
def index():
    with db.connect() as conn:
        conn.execute('select * from crime_info limit 1')
    return '''
        <h1>Hi</h1>
        '''

from server.routes.stations import StationRouter
from server.routes.crimes import CrimeRouter

app.register_blueprint(StationRouter)
app.register_blueprint(CrimeRouter)
