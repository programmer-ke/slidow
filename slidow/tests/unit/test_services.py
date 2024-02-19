import unittest

from slidow import services
from slidow.adapters import repos


class FakeSession:
    def commit(self):
        self.committed = True


class AddEventTestCase(unittest.TestCase):
    def test_can_add_event(self):
        event_name = "Some New Event"
        session = FakeSession()
        kv_store: dict[str, dict] = {}
        events_repo = repos.EventKeyValRepo(kv_store)

        event_identifier = services.add_event(event_name, session, events_repo)
        added_event = events_repo.get(event_identifier)
        self.assertEqual(event_name, added_event.name)

    def test_event_name_cannot_be_empty_string(self):

        event_name = ""
        session = FakeSession()
        kv_store: dict[str, dict] = {}
        events_repo = repos.EventKeyValRepo(kv_store)
        with self.assertRaises(
            services.InvalidEventNameError, msg="Event name cannot be empty string"
        ):
            services.add_event(event_name, session, events_repo)


if __name__ == "__main__":
    unittest.main()
