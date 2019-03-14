from flask import Flask, render_template, request, Blueprint
from routes.crimes import CrimeRouter
from routes.stations import StationRouter
from os import getenv, path
import sqlalchemy
import logging
from dotenv import load_dotenv

load_dotenv('.flaskenv')
load_dotenv('.env')

app = Flask(__name__)

logger = logging.getLogger()

db_user = getenv('DB_USER'),
db_pass = getenv('DB_PASS'),
db_name = getenv('DB_NAME')
cloud_sql_connection_name = getenv('CLOUD_SQL_CONNECTION_NAME')

db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername='postgres+pg8000',
        username = db_user,
        password = db_pass,
        database = db_name,
        query={
            'unix_sock': '/cloudsql/{}'.format(cloud_sql_connection_name)
        },
    ),
    pool_size = 5,
    max_overflow = 10,
    pool_timeout = 30,
    pool_recycle = 1800
)

app.register_blueprint(CrimeRouter)
app.register_blueprint(StationRouter)

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

@app.route('/', methods=['GET'])
def index():
    return '''
        <div style="text-align:center">
            <h1>Flask Server Running in Dev Mode</h1>
            <h2>Change value of FLASK_ENV in the .flaskenv file to run in Production Mode</h2>
        </div>
    '''

if __name__ == "__main__":
    debug = True if getenv('FLASK_ENV') else False
    app.run(port=getenv('FLASK_RUN_PORT'), debug=debug)