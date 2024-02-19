import unittest

from sqlalchemy import text as T

from slidow.adapters import orm
from slidow.entrypoints.flask_app import create_app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):

        # db prep
        self.app = create_app({"TESTING": True, "db_name": "slidow-test.sqlite"})
        Session = self.app.config["DB_SESSION_FACTORY"]
        bound_engine = Session.get_bind()
        orm.mapper_registry.metadata.create_all(bound_engine)

        self.client = self.app.test_client()
        self.session = Session()

    def tearDown(self):

        # db cleanup
        self.session.close()
        Session = self.app.config["DB_SESSION_FACTORY"]
        bound_engine = Session.get_bind()
        orm.mapper_registry.metadata.drop_all(bound_engine)
        Session = self.app.config["DB_SESSION_FACTORY"]
        Session.remove()

    def test_can_load_app(self):
        self.assertFalse(create_app().testing)
        self.assertTrue(create_app({"TESTING": True}).testing)

    def test_can_access_landing_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_can_list_all_events(self):
        events = ["Event1", "Event2"]

        for event in events:
            self.client.post("/events", data={"name": event})

        response = self.client.get("/events")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Event1", response.text)
        self.assertIn("Event2", response.text)

    def test_can_add_an_event(self):

        response = self.client.post("/events", data={"name": "Event1"})
        self.assertEqual(response.status_code, 302)

        response = self.client.get("/events")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Event1", response.text)

    def test_must_specify_event_name(self):

        response = self.client.post("/events")
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
