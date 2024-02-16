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

        new_event = services.add_event(event_name, session, events_repo)

        self.assertEqual(event_name, kv_store["events"][new_event.identifier].name)


if __name__ == "__main__":
    unittest.main()
