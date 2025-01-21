import sys
sys.path.insert(0, "..")
from main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_list_task():
    response = client.get("/tasks/list/")

    assert response.status_code == 200
    res = response.json()
    for i in ["data", "warning", "config", "buf"]:
        assert i in res

def test_status_task():
    response = client.get("/tasks/status/1/")

    assert response.status_code == 200
    res = response.json()
    for i in ["error", "data"]:
        assert i in res

def test_iocs_task():
    response = client.get("/tasks/iocs/1/")

    assert response.status_code == 200
    res = response.json()
    for i in ["error", "data"]:
        assert i in res



