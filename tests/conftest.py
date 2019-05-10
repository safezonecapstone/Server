import pytest
import subprocess
from connexion import FlaskApp
from flask_cors import CORS
from sqlalchemy import create_engine, engine
from os import getenv
from dotenv import load_dotenv
from ..server import create_app

@pytest.fixture
def db():

    load_dotenv('.flaskenv')
    load_dotenv('.env')

    URL = {
        'drivername': 'postgresql+pg8000',
        'username': getenv('LOCAL_USER'),
        'password': getenv('LOCAL_PASS'),
        'database': getenv('LOCAL_DB_NAME'),
    }

    db = create_engine(
        engine.url.URL(**URL),
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800
    )

    with db.connect() as conn:
        for table in ['crimes_by_station', 'crime_info', 'stations', 'crime_categories']:
            conn.execute(f'DELETE FROM {table} WHERE TRUE')

    return db

@pytest.fixture
def client():
    app = create_app('../')