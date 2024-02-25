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

class EventCreateTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_event_create(self):
        view = EventCreate.as_view()
        request = self.factory.post("/event/create/", {'id': 1})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        # Verificar si el event se ha creado correctamente

class RatingCreateTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.event = Event.objects.create()

    def test_rating_create(self):
        view = RatingCreate.as_view()
        request = self.factory.post("/rating/1/create/", {'content': 'New rating', 'event': self.event.id})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        # Verificar si el rating se ha creado correctamente

class EventDeleteTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.event = Event.objects.create()

    def test_event_delete(self):
        view = EventDelete.as_view()
        request = self.factory.delete(f"/event/{self.event.id}/delete/")
        response = view(request, pk=self.event.id)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())

class RatingDeleteTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.event = Event.objects.create()
        self.rating = Rating.objects.create(event=self.event, content="Evento")

    def test_message_delete(self):
        view = RatingDelete.as_view()
        request = self.factory.delete(f"/event/rating/{self.rating.id}/delete/")
        response = view(request, pk=self.rating.id)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Rating.objects.filter(id=self.rating.id).exists())
