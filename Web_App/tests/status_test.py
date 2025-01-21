import sys
sys.path.insert(0, "..")
from main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_status():
    response = client.get("/status/")

    assert response.status_code == 200
    res = response.json()
    for i in ["data", "status"]:
        assert i in res

def test_status():
    response = client.get("/status/win10/")

    assert response.status_code == 200
    res = response.json()
    for i in ["name", "id"]:
        assert i in res