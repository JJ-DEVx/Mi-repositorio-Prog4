import unittest
from app import app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_get_vacunas(self):
        response = self.client.get('/vacunas')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()