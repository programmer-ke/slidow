import unittest

from slidow.adapters import repos
from slidow.service_layer import services, unit_of_work


class AddEventTestCase(unittest.TestCase):

    def test_can_add_event(self):
        event_name = "Some New Event"

        uow = unit_of_work.DummyUOW()
        event_identifier = services.add_event(event_name, uow)
        self.assertTrue(uow.committed)
        added_event = uow.events.get(event_identifier)
        self.assertEqual(event_name, added_event.name)

    def test_event_name_cannot_be_empty_string(self):

        event_name = ""
        uow = unit_of_work.DummyUOW()

        with self.assertRaises(
            services.InvalidEventNameError, msg="Event name cannot be empty string"
        ):
            services.add_event(event_name, uow)


class ListEventTestCase(unittest.TestCase):

    def test_can_list_events(self):

        events = ["Event1", "Event2"]

        uow = unit_of_work.DummyUOW()
        for name in events:
            services.add_event(name, uow)

        event_repo = repos.EventKeyValRepo(uow.events.kv_store)  # type: ignore[attr-defined]
        retrieved_events = services.get_events(event_repo)
        event_names = [name for _, name in retrieved_events]
        self.assertIn("Event1", event_names)


if __name__ == "__main__":
    unittest.main()
