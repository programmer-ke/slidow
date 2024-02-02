import unittest
import slide_ow as domain


class EventTestCase(unittest.TestCase):
    def test_can_create_event(self):
        event = domain.Event(name="foo", identifier="event1")
        self.assertTrue((event.identifier, event.name), ("event1", "foo"))

    def test_two_events_with_same_name_are_different(self):
        event1 = domain.Event("event1", "foo")
        event2 = domain.Event("event2", "foo")

        self.assertFalse(event1 == event2)
        self.assertTrue(event1 == event1)

    def test_two_events_with_same_id_are_same(self):
        event1 = domain.Event("event1", "foo")
        event2 = domain.Event("event1", "foo")

        self.assertTrue(event1 == event2)

    def test_event_initialized_with_no_quizzes(self):
        id_, title = "event1", "warmup quiz"
        event = domain.Event(id_, title)

        self.assertEqual(event.quizzes, [])


class QuizTestCase(unittest.TestCase):

    def test_can_create_quiz(self):
        title = "warmup quiz"
        quiz = domain.Quiz(title, [])
        self.assertEqual(title, quiz.title)

    def test_can_add_questions_to_quiz(self):

        title = "warmup quiz"
        option1 = domain.Option(text="Bitcoin ETF")
        question1 = domain.Question("What is trending most on X?", [option1])
        quiz = domain.Quiz(title, [question1])

        question2 = domain.Question("Who is the best movie of all time?", [option1])
        quiz.questions.append(question2)
        self.assertEqual(quiz.questions, [question1, question2])


class QuestionTestCase(unittest.TestCase):

    def test_can_create_question_with_options(self):
        text = "What is trending most on X?"
        option1 = domain.Option(text="Bitcoin ETF")
        option2 = domain.Option(text="Elon Musk")
        question = domain.Question(text, [option1, option2])
        self.assertEqual(question.options, [option1, option2])

    def test_no_options_throws_error(self):
        text = "What is trending most on X?"
        with self.assertRaises(TypeError):
            question = domain.Question(text=text)  # type: ignore[call-arg]


class OptionTestCase(unittest.TestCase):
    def test_can_create_question_option(self):
        text = "Bitcoin ETF"
        option = domain.Option(text=text)
        self.assertEqual(option.text, text)
        self.assertEqual(option.correct, False)

    def test_can_specify_correct_option(self):
        option = domain.Option(text="Bitcoin ETF", correct=True)
        self.assertTrue(option.correct)


# class RepositoryTestCase(unittest.TestCase):
#
#    def test_can_save_an_event(self):
#        key_value_store = {}
#        repo = repository.EventKeyValueRepo(key_value_store)
#
#        repo.add(domain.Event(name="Friday Hangout"))
#
#        events = key_value_store["events"]
#        self.assertEqual()

if __name__ == "__main__":
    unittest.main()
