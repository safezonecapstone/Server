from dotenv import load_dotenv
from os import getenv
import sqlalchemy
from flask import Flask, redirect
import logging
from connexion import App

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

app = App(__name__, specification_dir='./')
app.add_api('swagger.yml')

logger = logging.getLogger()

@app.route('/')
@app.route('/api')
def index():
    return redirect('/api/ui')
