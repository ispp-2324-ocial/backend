from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .models import Event, Rating
from .views import *

# Create your tests here.

class EventListTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.event1 = Event.objects.create()
        self.event2 = Event.objects.create()

    def test_event_list(self):
        view = EventList.as_view()
        request = self.factory.get("/event/list/")
        response = view(request)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(len(data), 2)  # Verificar que se devuelvan todos los event
        
class RatingListTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.rating1 = Rating.objects.create()
        self.rating2 = Rating.objects.create()

    def test_rating_list(self):
        view = RatingList.as_view()
        request = self.factory.get("/rating/list/")
        response = view(request)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(len(data), 2)  # Verificar que se devuelvan todos los rating
