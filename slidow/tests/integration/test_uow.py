"""Unit of work tests"""

import unittest

from sqlalchemy import create_engine
from sqlalchemy import text as T
from sqlalchemy.orm import sessionmaker

from slidow import models
from slidow.adapters import orm
from slidow.service_layer import unit_of_work


class SQLAlchemyUOWTestCase(unittest.TestCase):

    def setUp(self):

        self.engine = create_engine("sqlite:///:memory:")
        orm.mapper_registry.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)

    def tearDown(self):

        orm.mapper_registry.metadata.drop_all(self.engine)

    def test_uow_can_add_an_event(self):

        with unit_of_work.SQLAlchemyUOW(self.session_factory) as uow:
            uow.events.add(models.Event("event1", "Event1"))
            uow.commit()

        session = self.session_factory()
        result = session.execute(T("SELECT identifier, name FROM event"))
        [(identifier, name)] = list(result)
        self.assertEqual(identifier, "event1")
        self.assertEqual(name, "Event1")

    def test_uncommitted_transactions_not_persisted(self):

        with unit_of_work.SQLAlchemyUOW(self.session_factory) as uow:
            uow.events.add(models.Event("event1", "Event1"))

        new_session = self.session_factory()
        results = list(new_session.execute(T("SELECT * FROM event")))
        self.assertEqual(results, [])

    def test_raised_exception_causes_rollback(self):

        class MyException(Exception):
            pass

        with self.assertRaises(MyException):
            with unit_of_work.SQLAlchemyUOW(self.session_factory) as uow:
                uow.events.add(models.Event("event1", "Event1"))
                raise MyException()
                uow.commit()

        new_session = self.session_factory()
        results = list(new_session.execute(T("SELECT * FROM event")))
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
