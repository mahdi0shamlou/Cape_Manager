import sys
sys.path.insert(0, "..")
from main import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_machines_start():
    response = client.post("/machines/start/win10-1/")

    assert response.status_code == 200
    res = response.json()
    for i in ["message"]:
        assert i in res

def test_machines_stop():
    response = client.post("/machines/stop/win10-1/")

    assert response.status_code == 200
    res = response.json()
    for i in ["message"]:
        assert i in res