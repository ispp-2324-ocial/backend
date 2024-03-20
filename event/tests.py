from django.test import TestCase

from django.contrib.auth.models import User
from ocial.models import TypeClient
from user.models import OcialClient
from .models import Event

class EventTestCase(TestCase):
    def setUp(self):
        # Crear un usuario de Django
        self.user = User.objects.create_user(
            username="ocialuser",
            email="ocialuser@example.com",
            password="password123",
        )

        # Datos del cliente
        self.client = OcialClient.objects.create(
            djangoUser=self.user,
            name="A",
            identificationDocument="X1234567A",
            typeClient=TypeClient.BAR_RESTAURANT.value,
            defaultLatitude=40.7128,
            defaultLongitude=-74.006,
        )

        self.event_data = {
            "name": "Football Match",
            "place": "Stadium ABC",
            "description": "Match between Team A and Team B",
            "date": "2024-02-25",
            "hour": "15:00:00",
            "capacity": 50000,
            "category": "SPORTS",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "ocialClient": self.client,  # Pasar la instancia del cliente en lugar de un ID
        }

    def test_create_client(self):
        self.assertEqual(OcialClient.objects.count(), 1)
        self.assertEqual(self.client.name, "A")
        # Añadir más aserciones para otros campos

    def test_create_event(self):
        event = Event.objects.create(**self.event_data)
        self.assertEqual(Event.objects.count(), 1)
        # Añadir aserciones adicionales si es necesario

    def test_delete_event(self):
        event = Event.objects.create(**self.event_data)
        event.delete()
        self.assertEqual(Event.objects.count(), 0)

