import sys
sys.path.insert(0, "..")
from main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_status_cape():
    response = client.get("/cape/status/")

    assert response.status_code == 200
    res = response.json()
    for i in ["status", "active", "loaded", "main_pid"]:
        assert i in res

def test_restart_cape():
    response = client.post("/cape/restart/")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Cape service restarted successfully."}



