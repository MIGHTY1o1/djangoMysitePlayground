import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
from django.urls import reverse


# testing Question view
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    # if pub date in before 1 day of the current date
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


# testing index view
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        # Correct the key to match the context_object_name in IndexView
        self.assertQuerysetEqual(response.context["latest_question_lst"], [])
        latest_question_lst = response.context["latest_question_lst"]
        print(
            "Test 'test_no_questions' successful! Latest Question List:",
            list(latest_question_lst),
        )

    # create question
    def create_question(self, question_text, days):
        """
        Create a question with the given `question_text` and published the
         given number of `days` offset to now (negative for questions published
        in the past, positive for questions that have yet to be published).
        """
        time = timezone.now() + datetime.timedelta(days=days)
        question = Question.objects.create(question_text=question_text, pub_date=time)
        print(f"Test 'question created' successful! Question: {question}")
        return question

    # test past question
    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = self.create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_lst"],
            [question],
        )
        latest_question_lst = response.context["latest_question_lst"]
        print(f"Test_past_question! latest_question_list: {latest_question_lst}")
        return question

    # test future question
    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        self.create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_lst"], [])
        latest_question_lst = response.context["latest_question_lst"]
        print(f"Test_future_question! latest_question_list: {latest_question_lst}")

    # test future question and past question
    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = self.create_question(question_text="Past question.", days=-30)
        self.create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_lst"],
            [question],
        )
        latest_question_lst = response.context["latest_question_lst"]
        print(
            f"Test_future_question_and_past_question! latest_question_list: {latest_question_lst}"
        )

    # test two past questions
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = self.create_question(question_text="Past question 1.", days=-30)
        question2 = self.create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_lst"],
            [question2, question1],
        )
        latest_question_lst = response.context["latest_question_lst"]
        print(f"test_two_past_questions! latest_question_list: {latest_question_lst}")


# Testing the DetailView
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = self.create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # latest_question_lst = response.context["latest_question_lst"]
        print(f"test_future_question!")

    # create question
    def create_question(self, question_text, days):
        """
        Create a question with the given `question_text` and published the
         given number of `days` offset to now (negative for questions published
        in the past, positive for questions that have yet to be published).
        """
        time = timezone.now() + datetime.timedelta(days=days)
        question = Question.objects.create(question_text=question_text, pub_date=time)
        print(f"Test 'question created' successful! Question: {question}")
        return question

    # test past question
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = self.create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        # latest_question_lst = response.context["latest_question_lst"]
        print(f"test_past_question!")
