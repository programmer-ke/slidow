import unittest

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker

from adapters import orm, repos
import slidow

Session = sessionmaker()

engine = create_engine("sqlite:///:memory:")


# The following event listeners are workarounds
# to pysqlite's bugs that prevent proper
# transaction handling
@event.listens_for(engine, "connect")
def do_connect(dbapi_connection, connection_record):
    # disable pysqlite's emitting of the BEGIN statement entirely.
    # also stops it from emitting COMMIT before any DDL.
    dbapi_connection.isolation_level = None


@event.listens_for(engine, "begin")
def do_begin(conn):
    # emit our own BEGIN
    conn.exec_driver_sql("BEGIN")


orm.mapper_registry.metadata.create_all(engine)


class SQLAlchemyRepositoryTestCase(unittest.TestCase):

    def setUp(self):
        self.connection = engine.connect()

        # begin a non-orm transaction
        self.transaction = self.connection.begin()

        # join transaction with savepoint (nested session)
        # any calls to Session.rollback will reset to savepoint
        self.session = Session(
            bind=self.connection, join_transaction_mode="create_savepoint"
        )

    def tearDown(self):
        self.session.close()

        # rollback everything including
        # calls to Session.commit
        self.transaction.rollback()
        self.connection.close()

    def test_can_save_an_event(self):

        event = slidow.Event("event1", "Friday Funday")
        repo = repos.EventSQLAlchemyRepo(self.session)

        repo.add(event)
        self.session.commit()

        result = self.session.execute(text('SELECT identifier, name FROM "event"'))

        rows = list(result)
        self.assertEqual(rows, [("event1", "Friday Funday")])

    def test_can_get_an_event(self):

        event = slidow.Event("event1", "Friday Hangout")
        self.insert_event(self.session, event.identifier, event.name)
        repo = repos.EventSQLAlchemyRepo(self.session)
        retrieved_event = repo.get("event1")

        self.assertEqual(retrieved_event, event)

    def test_can_get_an_event_list(self):

        event1 = slidow.Event("event1", "Friday Hangout")
        event2 = slidow.Event("event2", "Happy Hour")
        self.insert_event(self.session, event1.identifier, event1.name)
        self.insert_event(self.session, event2.identifier, event2.name)
        repo = repos.EventSQLAlchemyRepo(self.session)

        retrieved_events = repo.list()

        self.assertTrue(event1 in retrieved_events)
        self.assertTrue(event2 in retrieved_events)

    def test_can_save_a_quiz(self):
        quiz = self.create_quiz()

        repo = repos.QuizSQLAlchemyRepo(self.session)

        repo.add(quiz)
        self.session.commit()

        result = self.session.execute(text('SELECT identifier, title FROM "quiz"'))
        rows = list(result)
        self.assertEqual(rows, [(quiz.identifier, quiz.title)])

        question = quiz.questions[0]
        result = self.session.execute(text('SELECT text FROM "question"'))
        rows = list(result)
        self.assertEqual(rows, [(question.text,)])

        option1, option2 = question.options
        result = self.session.execute(text('SELECT text, correct FROM "option"'))
        rows = list(result)
        self.assertEqual(
            rows, [(option1.text, option1.correct), (option2.text, option2.correct)]
        )

    def test_can_get_a_quiz(self):

        quiz = self.create_quiz()
        [question] = quiz.questions
        option1, option2 = question.options

        quiz_id = self.insert_quiz(self.session, quiz.identifier, quiz.title)
        question_id = self.insert_question(self.session, quiz_id, question.text)
        self.insert_option(self.session, question_id, option1.text, option1.correct)
        self.insert_option(self.session, question_id, option2.text, option2.correct)

        repo = repos.QuizSQLAlchemyRepo(self.session)
        retrieved_quiz = repo.get(quiz.identifier)

        self.assertEqual(retrieved_quiz, quiz)
        self.assertEqual(retrieved_quiz.questions, quiz.questions)

    def test_can_save_event_quiz(self):

        quiz = self.create_quiz()
        event = slidow.Event("event1", "Friday Funday", quizzes=[quiz])
        repo = repos.EventSQLAlchemyRepo(self.session)

        repo.add(event)
        self.session.commit()

        result = self.session.execute(text('SELECT identifier, name FROM "event"'))
        rows = list(result)
        self.assertEqual(rows, [("event1", "Friday Funday")])

        result = self.session.execute(text('SELECT identifier, title FROM "quiz"'))
        rows = list(result)
        self.assertEqual(rows, [(quiz.identifier, quiz.title)])

        question = quiz.questions[0]
        result = self.session.execute(text('SELECT text FROM "question"'))
        rows = list(result)
        self.assertEqual(rows, [(question.text,)])

        option1, option2 = question.options
        result = self.session.execute(text('SELECT text, correct FROM "option"'))
        rows = list(result)
        self.assertEqual(
            rows, [(option1.text, option1.correct), (option2.text, option2.correct)]
        )

    def create_quiz(self):
        option1 = slidow.Option("yes")
        option2 = slidow.Option("no", correct=True)

        question_text = "Is Bitcoin Dead?"
        question = slidow.Question(question_text, [option1, option2])

        return slidow.Quiz("quiz1", "warmup quiz", questions=[question])

    def insert_quiz(self, session, identifier, title) -> int:
        session.execute(
            text("INSERT INTO quiz (identifier, title) VALUES (:identifier, :title)"),
            dict(identifier=identifier, title=title),
        )
        [(quiz_id,)] = session.execute(
            text("SELECT id FROM quiz WHERE identifier=:identifier"),
            {"identifier": identifier},
        )
        return quiz_id

    def insert_question(self, session, quiz_id, question_text) -> int:
        session.execute(
            text("INSERT INTO question (quiz_id, text) VALUES (:quiz_id, :text)"),
            dict(quiz_id=quiz_id, text=question_text),
        )
        [(question_id,)] = session.execute(
            text("SELECT id FROM question WHERE quiz_id=:quiz_id"),
            {"quiz_id": quiz_id},
        )
        return question_id

    def insert_option(self, session, question_id, option_text, correct) -> int:
        session.execute(
            text(
                "INSERT INTO option (question_id, text, correct) VALUES (:question_id, :text, :correct)"
            ),
            dict(question_id=question_id, text=option_text, correct=correct),
        )
        [(option_id,)] = session.execute(
            text("SELECT id FROM option WHERE text=:text"),
            {"text": option_text},
        )
        return option_id

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


class KeyValRepositoryTestCase(unittest.TestCase):

    def test_can_save_an_event(self):
        key_value_store: dict[str, dict] = {}
        repo = repos.EventKeyValRepo(key_value_store)
        event = slidow.Event("event1", "Friday Hangout")

        repo.add(event)

        events = key_value_store["events"]
        self.assertEqual(events["event1"], event)

    def test_can_get_an_event(self):
        event = slidow.Event("event1", "Friday Hangout")

        key_value_store: dict[str, dict] = {"events": {"event1": event}}

        repo = repos.EventKeyValRepo(key_value_store)
        retrieved_event = repo.get("event1")

        self.assertEqual(retrieved_event, event)

    def test_can_get_list_of_events(self):
        event1 = slidow.Event("event1", "Friday Hangout")
        event2 = slidow.Event("event2", "Happy Hour Quiz")

        key_value_store: dict[str, dict] = {
            "events": {"event1": event1, "event2": event2}
        }

        repo = repos.EventKeyValRepo(key_value_store)
        retrieved_events = repo.list()

        self.assertTrue(event1 in retrieved_events)
        self.assertTrue(event2 in retrieved_events)

    def test_can_save_a_quiz(self):
        text = "What is trending most on X?"
        option1 = slidow.Option(text="Bitcoin ETF", correct=True)
        option2 = slidow.Option(text="Elon Musk")
        question = slidow.Question(text, [option1, option2])
        title = "warmup quiz"
        quiz = slidow.Quiz("quiz1", title, [question])

        kv_store: dict[str, dict] = {}
        repo = repos.QuizKeyValRepo(kv_store)

        repo.add(quiz)

        quizzes = kv_store["quizzes"]
        self.assertEqual(quizzes["quiz1"], quiz)

    def test_can_get_a_quiz(self):
        text = "What is trending most on X?"
        option1 = slidow.Option(text="Bitcoin ETF", correct=True)
        option2 = slidow.Option(text="Elon Musk")
        question = slidow.Question(text, [option1, option2])
        title = "warmup quiz"
        quiz = slidow.Quiz("quiz1", title, [question])

        key_value_store: dict[str, dict] = {"quizzes": {"quiz1": quiz}}

        repo = repos.QuizKeyValRepo(key_value_store)
        retrieved_quiz = repo.get("quiz1")

        self.assertEqual(retrieved_quiz, quiz)


if __name__ == "__main__":
    unittest.main()
