import datetime
from venv import create

from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls.base import reverse

# Create your tests here.


class QuestionModelTest(TestCase):

    def test_was_published_recently(self):
        """
        Verifica que la variable future_question devuelva true si fue creada recientemente como se estipulo en el metodo was_published_recently de models.py de lo contrario deberia dar un assert error
        """
        
        time = timezone.now() + datetime.timedelta(days= 30)
        future_question = Question(question_text= "Cual es el mejor CD de platzi?", pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

#Funcion para crear preguntas
def create_question(question_text, days):
    """Esta funcion creara una pregunta indicandole el tiempo, pasado o futuro indicado en el parametro days de su publicacion evaluando si el numero es negativo o positivo partiendo del tiempo presente para definir si sera pasado o futuro"""

    time = timezone.now() + datetime.timedelta(days= days)
    return Question.objects.create(question_text=question_text, pub_date= time)
     

class QuestionIndexViewTest(TestCase):

    """Si no existen preguntas un error se disparara"""

    def test_no_question(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "No esta disponible")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])


    def test_future_question(self):
        """Preguntas con fecha de publicacion en futuro no seran publicadas en nuestro index"""
        create_question("Present Question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No esta disponible")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])


    def test_past_question(self):
        """ Cuando se publiquen preguntas con fecha del pasado estas deben aparecer en nuestra index"""

        question = create_question("Past Question", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])


    def test_future_past_question(self):
        question_future = create_question(question_text="This question is the future", days=30)
        question_past = create_question(question_text="This question is the past", days=-30)
        response= self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question_past])



    def test_two_past_question(self):
        question_past1 = create_question(question_text="This question is the past", days=-30)
        question_past2 = create_question(question_text="This question is the past2", days= -1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question_past1, question_past2])


    def test_two_future(self):
        question_future1 = create_question(question_text="This question is the future1", days=30)
        question_future2 = create_question(question_text="This question is the future2", days=1)
        response= self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    