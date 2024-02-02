import unittest

import repos
import slidow


class EventTestCase(unittest.TestCase):
    def test_can_create_event(self):
        event = slidow.Event(name="foo", identifier="event1")
        self.assertTrue((event.identifier, event.name), ("event1", "foo"))

    def test_two_events_with_same_name_are_different(self):
        event1 = slidow.Event("event1", "foo")
        event2 = slidow.Event("event2", "foo")

        self.assertFalse(event1 == event2)
        self.assertTrue(event1 == event1)

    def test_two_events_with_same_id_are_same(self):
        event1 = slidow.Event("event1", "foo")
        event2 = slidow.Event("event1", "foo")

        self.assertTrue(event1 == event2)

    def test_event_initialized_with_no_quizzes(self):
        id_, title = "event1", "warmup quiz"
        event = slidow.Event(id_, title)

        self.assertEqual(event.quizzes, [])


class QuizTestCase(unittest.TestCase):

    def test_can_create_quiz(self):
        title = "warmup quiz"
        quiz = slidow.Quiz("quizid", title, [])
        self.assertEqual(title, quiz.title)

    def test_can_add_questions_to_quiz(self):

        title = "warmup quiz"
        option1 = slidow.Option(text="Bitcoin ETF")
        question1 = slidow.Question("What is trending most on X?", [option1])
        quiz = slidow.Quiz("quiz1", title, [question1])

        question2 = slidow.Question("Who is the best movie of all time?", [option1])
        quiz.questions.append(question2)
        self.assertEqual(quiz.questions, [question1, question2])

    def test_can_create_question_with_options(self):
        text = "What is trending most on X?"
        option1 = slidow.Option(text="Bitcoin ETF")
        option2 = slidow.Option(text="Elon Musk")
        question = slidow.Question(text, [option1, option2])
        self.assertEqual(question.options, [option1, option2])

    def test_no_options_throws_error(self):
        text = "What is trending most on X?"
        with self.assertRaises(TypeError):
            question = slidow.Question(text=text)  # type: ignore[call-arg]

    def test_can_create_question_option(self):
        text = "Bitcoin ETF"
        option = slidow.Option(text=text)
        self.assertEqual(option.text, text)
        self.assertEqual(option.correct, False)

    def test_can_specify_correct_option(self):
        option = slidow.Option(text="Bitcoin ETF", correct=True)
        self.assertTrue(option.correct)


class RepositoryTestCase(unittest.TestCase):

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
