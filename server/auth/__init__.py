from os import getenv

def authenticated(apikey, required_scopes):
    if apikey == getenv('API_KEY'):
        return { 'isAuthenticated': True }
    return None