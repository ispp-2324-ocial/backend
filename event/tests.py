from django.test import TestCase

from django.contrib.auth.models import User
from ocial.models import Category, TypeClient
from user.models import OcialClient
from .models import Event
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

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
            "timeStart": "2024-02-25 15:00:00",
            "timeEnd": "2024-02-25 17:00:00",
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

    def test_event_str_representation(self):
        event = Event.objects.create(**self.event_data)
        expected_str = f"{event.name}: {event.event} | {event.timeStart} -> {event.timeEnd}"
        self.assertEqual(str(event), expected_str)

    def test_event_default_capacity(self):
        event = Event.objects.create(**self.event_data)
        self.assertEqual(event.capacity, 50000)

    def test_event_category_choices(self):
        event = Event.objects.create(**self.event_data)
        categories = dict(event._meta.get_field('category').choices)
        self.assertIn(event.category, categories.values())

    def test_invalid_capacity(self):
        self.event_data['capacity'] = -100  # Valor de capacidad inválido
        with self.assertRaises(IntegrityError):
            Event.objects.create(**self.event_data)

    def test_invalid_date(self):
        self.event_data['timeStart'] = '2023-02-30 15:00:00'  # Fecha inválida (30 de febrero)
        with self.assertRaises(ValidationError):
            Event.objects.create(**self.event_data)

    def test_invalid_hour(self):
        self.event_data['timeStart'] = '2023-02-25 25:00:00'  # Hora inválida
        with self.assertRaises(ValidationError):
            Event.objects.create(**self.event_data)


