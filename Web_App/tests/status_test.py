#----------------- interperter config
import sys
sys.path.insert(0, '..')
#--------------------------------
import sys
from unittest.mock import patch, MagicMock
import unittest
from fastapi.testclient import TestClient
from main import app
# --------------------------------

class TestStatusEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('libvirt.open')
    def test_read_status(self, mock_open):
        # Create a mock connection and domain
        mock_conn = MagicMock()
        mock_domain = MagicMock()

        # Set up the mock domain return values
        mock_domain.name.return_value = "test-vm"
        mock_domain.ID.return_value = 1
        mock_domain.state.return_value = (1, None)  # Running state

        # Set up the mock connection return values
        mock_conn.listAllDomains.return_value = [mock_domain]
        mock_open.return_value = mock_conn

        # Call the endpoint
        response = self.client.get("/status/")

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
        expected_response = [
            {
                'name': "test-vm",
                'id': 1,
                'state': 1  # Corresponds to running state
            }
        ]
        self.assertEqual(response.json(), expected_response)


if __name__ == "__main__":
    unittest.main()
