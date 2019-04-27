import pytest
from sqlalchemy import create_engine, engine
from os import getenv
from server.models import create_db

@pytest.fixture
def db():
    return create_db(test=True)

