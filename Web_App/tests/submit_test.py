import sys
sys.path.insert(0, "..")
from main import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_submit():
    # Create a sample file content
    sample_file_content = b"Sample file content"
    sample_file_name = "sample.txt"

    # Create a dictionary to hold the files and form data
    files = {
        "file": (sample_file_name, sample_file_content, "text/plain"),  # (filename, content, content-type)
    }
    data = {
        "machine_name": "win10-3",
    }

    # Send a POST request to the /submit/ endpoint
    response = client.post("/submit/", files=files, data=data)

    # Check the response status code
    assert response.status_code == 200

    # Check the response JSON for expected keys
    res = response.json()
    for key in ["task_id", "message"]:
        assert key in res
