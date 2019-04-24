import pytest
from sqlalchemy import create_engine, engine
from os import getenv

@pytest.fixture
def db():
    return create_engine(
        engine.url.URL(
            drivername='postgres+pg8000',
            username=getenv('DB_TEST_USER'),
            password=getenv('DB_TEST_PASS'),
            database=getenv('DB_TEST_NAME'),
            query={
            'unix_sock': getenv('DB_TEST_SOCKET_URL')
            }
        ),
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800
    )

