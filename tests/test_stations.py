from os import getenv

def test_nearby_stations(db, client):
    api_key = getenv('API_KEY')
    res = client.get(f'/api/stations/nearby?latitude=40.768563&latitude=-73.964429&API_KEY={api_key}')
    assert res.data == {}