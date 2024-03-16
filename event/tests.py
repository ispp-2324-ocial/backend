from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import Event, OcialClient, Rating
from .serializers import EventSerializer, RatingSerializer

class EventTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.ocial_client = OcialClient.objects.create(
            usuario=self.user,
            default_latitude=0.0,
            default_longitude=0.0  
        )

    def test_create_event(self):
        url = reverse('event_create')
        data = {
            'name': 'Test Event',
            'place': 'Test Place',
            'event': 'Test Event Description',
            'date': '2024-03-16',
            'hour': '12:00:00',
            'capacity': 100,
            'category': 'Sports',
            'latitude': 40.0,
            'longitude': -40.0,
            'ocialClient': {
                'default_latitude': 0.0,  
                'default_longitude': 0.0  
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_events(self):
        Event.objects.create(
            name='Test Event',
            place='Test Place',
            event='Test Event Description',
            date='2024-03-16',
            hour='12:00:00',
            capacity=100,
            category='Sports',
            latitude=40.0,
            longitude=-40.0,
            ocialClient=self.ocial_client
        )
        url = reverse('event_list')
        response = self.client.get(url)
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_event(self):
        event = Event.objects.create(
            name='Test Event',
            place='Test Place',
            event='Test Event Description',
            date='2024-03-16',
            hour='12:00:00',
            capacity=100,
            category='Sports',
            latitude=40.0,
            longitude=-40.0,
            ocialClient=self.ocial_client
        )
        url = reverse('event_update', kwargs={'pk': event.pk})
        data = {
            'name': 'Updated Test Event',
            'place': 'Updated Test Place',
            'event': 'Updated Test Event Description',
            'date': '2024-03-16',
            'hour': '13:00:00',
            'capacity': 150,
            'category': 'Music',
            'latitude': 45.0,
            'longitude': -45.0,
            'ocialClient': {  
                'default_latitude': 0.0,  
                'default_longitude': 0.0  
            }
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_event(self):
        event = Event.objects.create(
            name='Test Event',
            place='Test Place',
            event='Test Event Description',
            date='2024-03-16',
            hour='12:00:00',
            capacity=100,
            category='Sports',
            latitude=40.0,
            longitude=-40.0,
            ocialClient=self.ocial_client
        )
        url = reverse('event_delete', kwargs={'pk': event.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_events_by_client(self):
        url = reverse('event_list_by_client', kwargs={'pk': self.ocial_client.pk})
        response = self.client.get(url)
        events = Event.objects.filter(ocialClient=self.ocial_client)
        serializer = EventSerializer(events, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class EventNearbyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.ocial_client = OcialClient.objects.create(
            usuario=self.user,
            default_latitude=0.0,
            default_longitude=0.0
        )

    def test_list_events_nearby(self):
        # Crear eventos de prueba
        event1 = Event.objects.create(
            name='Test Event 1',
            place='Test Place 1',
            event='Test Event Description 1',
            date='2024-03-16',
            hour='12:00:00',
            capacity=100,
            category='Sports',
            latitude=40.0,
            longitude=-40.0,
            ocialClient=self.ocial_client
        )
        Event.objects.create(
            name='Test Event 2',
            place='Test Place 2',
            event='Test Event Description 2',
            date='2024-03-16',
            hour='12:00:00',
            capacity=100,
            category='Sports',
            latitude=42.0,
            longitude=-42.0,
            ocialClient=self.ocial_client
        )

        url = reverse('event_nearby')
        data = {'latitude': 40.0, 'longitude': -40.0, 'radius': 10.0}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], event1.id)

class RatingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        self.ocial_client = OcialClient.objects.create(
            usuario=self.user,
            default_latitude=0.0,
            default_longitude=0.0
        )

        self.event = Event.objects.create(
            name='Test Event',
            place='Test Place',
            event='Test Event Description',
            date='2024-03-16',
            hour='12:00:00',
            capacity=100,
            category='Sports',
            latitude=40.0,
            longitude=-40.0,
            ocialClient=self.ocial_client
        )
        
        self.rating1 = Rating.objects.create(score=4, comment='Great event!', event=self.event)
        self.rating2 = Rating.objects.create(score=5, comment='Excellent!', event=self.event)

    def test_list_ratings(self):
        url = reverse('rating_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_rating(self):
        url = reverse('rating_create')
        data = {'score': 4, 'comment': 'Great event!', 'event': self.event.pk}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_rating(self):
        rating = Rating.objects.create(score=4, comment='Great event!', event=self.event)
        url = reverse('rating_delete', kwargs={'pk': rating.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
