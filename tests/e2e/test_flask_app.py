import unittest

from entrypoints.flask_app import create_app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    def test_can_load_app(self):
        self.assertFalse(create_app().testing)
        self.assertTrue(create_app({"TESTING": True}).testing)

    def test_can_access_landing_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
