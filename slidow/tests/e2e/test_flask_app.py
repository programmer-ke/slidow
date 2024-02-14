import unittest

from sqlalchemy import text

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

    def insert_event(self, session, identifier, name) -> int:
        session.execute(
            text("insert into event (identifier, name)" " values (:identifier, :name)"),
            dict(identifier=identifier, name=name),
        )
        (event_id,) = session.execute(
            text("select id from event" " where identifier=:identifier"),
            {"identifier": identifier},
        )
        return event_id

    def test_can_load_app(self):
        self.assertFalse(create_app().testing)
        self.assertTrue(create_app({"TESTING": True}).testing)

    def test_can_access_landing_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_can_see_events_list(self):
        events = [("event1", "Event1"), ("event2", "Event2")]

        for event in events:
            self.insert_event(self.session, *event)

        response = self.client.get("/events")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Event1", response.text)
        self.assertIn("Event2", response.text)


if __name__ == "__main__":
    unittest.main()
