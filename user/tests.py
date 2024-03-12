from django.test import TestCase
from .models import OcialUser, OcialClient
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

class OcialUserTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            "ocialuser1", "chevy@chase.com", "chevyspassword"
        )
        self.user_2 = User.objects.create_user(
            "ocialuser2", "chevy@chase.com", "chevyspassword"
        )
        self.user_3 = User.objects.create_user(
            "ocialuser3", "chevy@chase.com", "chevyspassword"
        )
        self.user_4 = User.objects.create_user(
            "ocialuser4", "chevy@chase.com", "chevyspassword"
        )

        self.user1= OcialUser.objects.create(
            usuario=self.user_1,
            lastKnowLocLat=40.0,
            lastKnowLocLong=45.0,
        )

        self.user2 = OcialClient.objects.create(
            usuario=self.user_2,
            name="asjodbgfaodvhier",
            identification_document="A12345678",  # cif
            typeClient=OcialClient.TypeClient.ARTIST,
            default_latitude=40.7128,
            default_longitude=-40.7128,
        )

        self.user3 = OcialClient.objects.create(
            usuario=self.user_3,
            name="A",
            identification_document="X1234567A",  # nie
            typeClient=OcialClient.TypeClient.BAR_RESTAURANT,
            default_latitude=40.7128,
            default_longitude=0.0,
        )

        self.user4 = OcialClient.objects.create(
            usuario=self.user_4,
            name="A",
            identification_document="12345678A",  # dni
            # Default typeClient
            default_latitude=-40.7128,
            default_longitude=0.0,
        )

        self.list1 = [self.user1, self.user2, self.user3, self.user4]

        self.client = APIClient()
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
            "lastKnowLocLat": 40.7128,
            "lastKnowLocLong": -40.7128,
            "typesfavEventType": OcialUser.TypesfavEvent.MUSIC,
        }
        self.client_data = {
            "username": "testclient",
            "password": "testpassword",
            "email": "client@example.com",
            "name": "Test Client",
            "identification_document": "09981078K",
            "typeClient": OcialClient.TypeClient.ARTIST,
            "default_latitude": 40.7128,
            "default_longitude": -40.7128,
        }

    def test_get_users(self):
        self.list2 = [self.user1, self.user2, self.user3, self.user4]
        self.assertEqual(self.list1, self.list2)
        self.assertEqual(self.user4.typeClient, OcialClient.TypeClient.SMALL_BUSINESS)

    def test_create_user(self):
        response = self.client.post("/api/users/user/register/", self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_create_client(self):
        response = self.client.post("/api/users/client/register/", self.client_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(username="testclient").exists())

    def test_login_user(self):
        User.objects.create_user(username=self.user_data['username'], email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.post("/api/users/login/", {"username": "testuser", "password": "testpassword"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    # def test_logout_user(self):
    #     # Crear un usuario en la base de datos
    #     User.objects.create_user(username=self.user_data['username'], email=self.user_data['email'], password=self.user_data['password'])
        
    #     # Autenticar al usuario antes de intentar cerrar sesión
    #     self.client.login(username="testuser", password="testpassword")
        
    #     # Realizar la solicitud para cerrar sesión
    #     response = self.client.post("/api/users/logout/", format="json")
        
    #     # Verificar si la solicitud fue exitosa y si el token no está presente en la respuesta
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertFalse("token" in response.data)

    # def test_register_user_view(self):
    #     response = self.client.post("/api/register-user/", self.user_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue(User.objects.filter(username="testuser").exists())

    # def test_register_client_view(self):
    #     response = self.client.post("/api/register-client/", self.client_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue(User.objects.filter(username="testclient").exists())

