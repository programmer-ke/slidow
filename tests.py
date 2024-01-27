import unittest
import slide_ow


class EventTestCase(unittest.TestCase):
    def test_can_create_event(self):
        event = slide_ow.Event(name="foo")
        self.assertTrue(event.name, "foo")

    def test_two_events_with_same_name_are_different(self):
        event1 = slide_ow.Event(name="foo")
        event2 = slide_ow.Event(name="foo")

        self.assertFalse(event1 == event2)
        self.assertFalse(event1 is event2)
        self.assertTrue(event1 == event1)

    def test_can_add_quizes_to_event(self):
        title = "warmup quiz"
        quiz = slide_ow.Quiz(title=title)

        event = slide_ow.Event(name="foo")
        event.quiz = quiz
        self.assertTrue(event.quiz is quiz)


class QuizTestCase(unittest.TestCase):
    def test_can_create_quiz(self):
        title = "warmup quiz"
        quiz = slide_ow.Quiz(title=title)
        self.assertEqual(title, quiz.title)

    def test_can_add_questions_to_quiz(self):
        title = "warmup quiz"
        quiz = slide_ow.Quiz(title=title)
        self.assertTrue(quiz.questions is None)
        question1 = slide_ow.Question(text="What is trending most on X?")
        question2 = slide_ow.Question(text="Who is the best movie of all time?")

        quiz.questions = [question1, question2]
        self.assertEqual(quiz.questions, [question1, question2])


class QuestionTestCase(unittest.TestCase):
    def test_can_create_question(self):
        text = "What is trending most on X?"
        question = slide_ow.Question(text=text)
        self.assertEqual(question.text, text)

    def test_can_add_option_to_question(self):
        text = "What is trending most on X?"
        question = slide_ow.Question(text=text)
        option1 = slide_ow.Option(text="Bitcoin ETF")
        option2 = slide_ow.Option(text="Elon Musk")
        question.options = [option1, option2]
        self.assertEqual(question.options, [option1, option2])

    def test_no_options_gives_none(self):
        text = "What is trending most on X?"
        question = slide_ow.Question(text=text)
        self.assertTrue(question.options is None)


class OptionTestCase(unittest.TestCase):
    def test_can_create_question_option(self):
        text = "Bitcoin ETF"
        option = slide_ow.Option(text=text)
        self.assertEqual(option.text, text)
        self.assertEqual(option.correct, False)

    def test_can_specify_correct_option(self):
        option = slide_ow.Option(text="Bitcoin ETF", correct=True)
        self.assertTrue(option.correct)


if __name__ == "__main__":
    unittest.main()
