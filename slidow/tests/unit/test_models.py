import unittest

from slidow import models


class EventTestCase(unittest.TestCase):
    def test_can_create_event(self):
        event = models.Event(name="foo", identifier="event1")
        self.assertTrue((event.identifier, event.name), ("event1", "foo"))

    def test_two_events_with_same_name_are_different(self):
        event1 = models.Event("event1", "foo")
        event2 = models.Event("event2", "foo")

        self.assertFalse(event1 == event2)
        self.assertTrue(event1 == event1)

    def test_two_events_with_same_id_are_same(self):
        event1 = models.Event("event1", "foo")
        event2 = models.Event("event1", "foo")

        self.assertTrue(event1 == event2)

    def test_event_initialized_with_no_quizzes(self):
        id_, title = "event1", "warmup quiz"
        event = models.Event(id_, title)

        self.assertEqual(event.quizzes, [])

    def test_can_generate_new_identifiers(self):
        event_name = "Last Friday"
        event1 = models.Event.with_random_identifier(event_name)
        event2 = models.Event.with_random_identifier(event_name)
        self.assertEqual(event1.name, event2.name)
        self.assertNotEqual(event1.identifier, event2.identifier)


class QuizTestCase(unittest.TestCase):

    def test_can_create_quiz(self):
        title = "warmup quiz"
        quiz = models.Quiz("quizid", title, [])
        self.assertEqual(title, quiz.title)

    def test_can_add_questions_to_quiz(self):

        title = "warmup quiz"
        option1 = models.Option(text="Bitcoin ETF")
        question1 = models.Question("What is trending most on X?", [option1])
        quiz = models.Quiz("quiz1", title, [question1])

        question2 = models.Question("Who is the best movie of all time?", [option1])
        quiz.questions.append(question2)
        self.assertEqual(quiz.questions, [question1, question2])


class QuestionTestCase(unittest.TestCase):

    def test_can_create_question_with_options(self):
        text = "What is trending most on X?"
        option1 = models.Option(text="Bitcoin ETF")
        option2 = models.Option(text="Elon Musk")
        question = models.Question(text, [option1, option2])
        self.assertEqual(question.options, [option1, option2])

    def test_no_options_throws_error(self):
        text = "What is trending most on X?"
        with self.assertRaises(TypeError):
            question = models.Question(text=text)  # type: ignore[call-arg]


class OptionTestCase(unittest.TestCase):

    def test_can_create_question_option(self):
        text = "Bitcoin ETF"
        option = models.Option(text=text)
        self.assertEqual(option.text, text)
        self.assertEqual(option.correct, False)

    def test_can_specify_correct_option(self):
        option = models.Option(text="Bitcoin ETF", correct=True)
        self.assertTrue(option.correct)


if __name__ == "__main__":
    unittest.main()
