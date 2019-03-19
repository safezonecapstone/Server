from os import getenv
from server.models import db

def authenticated(apikey, required_scopes):
    if apikey == getenv('API_KEY'):
        return { 'isAuthenticated': True }
    return None