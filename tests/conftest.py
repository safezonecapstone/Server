import pytest
from server import create_app
from dotenv import load_dotenv

@pytest.fixture
def client():
    app = create_app()
    yield app.app.test_client()