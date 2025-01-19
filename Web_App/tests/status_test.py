#----------------- interperter config
import sys
sys.path.insert(0, '..')
#--------------------------------

import unittest
from fastapi.testclient import TestClient
from main import app

class TestStatusEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_status(self):
        response = self.client.get("/status/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"name": "Status Name"})

if __name__ == "__main__":
    unittest.main()
