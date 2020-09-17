import app
from chalice.test import Client

def test_index_route():
    with Client(app.app) as client:
        response = client.http.get('/')
        assert response.status.code == 200