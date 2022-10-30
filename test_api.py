from fastapi.testclient import TestClient

from api import app

client = TestClient(app)

# TODO: set-up test database
# TODO: fill test db with data

def test_artist_list():
    response = client.get("/artists/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    print(data)
    assert all((x.get("id") for x in data))
