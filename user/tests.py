from django.test import TestCase
from .models import OcialUser, OcialClient
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse


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

        self.user1 = OcialUser.objects.create(
            djangoUser=self.user_1,
            lastKnowLocLat=40.0,
            lastKnowLocLong=45.0,
        )

        self.user2 = OcialClient.objects.create(
            djangoUser=self.user_2,
            name="asjodbgfaodvhier",
            identificationDocument="A12345678",  # cif
            typeClient=OcialClient.TypeClient.ARTIST,
            defaultLatitude=40.7128,
            defaultLongitude=-40.7128,
        )

        self.user3 = OcialClient.objects.create(
            djangoUser=self.user_3,
            name="A",
            identificationDocument="X1234567A",  # nie
            typeClient=OcialClient.TypeClient.BAR_RESTAURANT,
            defaultLatitude=40.7128,
            defaultLongitude=0.0,
        )

        self.user4 = OcialClient.objects.create(
            djangoUser=self.user_4,
            name="A",
            identificationDocument="12345678A",  # dni
            # Default typeClient
            defaultLatitude=-40.7128,
            defaultLongitude=0.0,
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

    def testGetUsers(self):
        self.list2 = [self.user1, self.user2, self.user3, self.user4]
        self.assertEqual(self.list1, self.list2)
        self.assertEqual(self.user4.typeClient, OcialClient.TypeClient.SMALL_BUSINESS)

    def testCreateUser(self):
        response = self.client.post(
            "/api/users/user/register/", self.user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def testCreateClient(self):
        response = self.client.post(
            "/api/users/client/register/", self.client_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(username="testclient").exists())

    def testLoginUser(self):
        User.objects.create_user(
            username=self.user_data["username"],
            email=self.user_data["email"],
            password=self.user_data["password"],
        )
        response = self.client.post(
            "/api/users/login/",
            {"username": "testuser", "password": "testpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def testLogoutUser(self):
        user = User.objects.create_user(
            username=self.user_data["username"],
            email=self.user_data["email"],
            password=self.user_data["password"],
        )
        response = self.client.post(
            "/api/users/login/",
            {"username": user.username, "password": self.user_data["password"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data.get("token")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response = self.client.post("/api/users/logout/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=user).exists())

    def testCreateUserMissingUsername(self):
        # Try to create a user without username
        invalid_user_data = {
            "password": "testpassword",
            "email": "test@example.com",
            # Missing username
        }
        response = self.client.post(
            "/api/users/user/register/", invalid_user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCreateUserMissingEmail(self):
        # Try to create a user without username
        invalid_user_data = {
            "password": "testpassword",
            # Missing email
            "username": "test",
        }
        response = self.client.post(
            "/api/users/user/register/", invalid_user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCreateUserMissinPassword(self):
        # Try to create a user without username
        invalid_user_data = {
            # Missing password
            "email": "test@example.com",
            "username": "test",
        }
        response = self.client.post(
            "/api/users/user/register/", invalid_user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCreateClientInvalidData(self):
        # Try to create a client without name
        invalid_client_data = {
            "username": "testclient",
            "password": "testpassword",
            "email": "client@example.com",
            # Missing name
            "identification_document": "A12345678",
            "typeClient": OcialClient.TypeClient.ARTIST,
            "default_latitude": 40.7128,
            "default_longitude": -40.7128,
        }
        response = self.client.post(
            "/api/users/client/register/", invalid_client_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testLoginUserInvalidCredentials(self):
        invalid_credentials = {
            "username": "incorrect_username",
            "password": "incorrect_password",
        }
        response = self.client.post(
            "/api/users/login/", invalid_credentials, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testLogoutUserUnauthenticated(self):
        # Try to logout without auth
        response = self.client.post("/api/users/logout/", format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testRegisterUserDuplicateUsername(self):
        User.objects.create_user(username="testuser", password="testpassword")
        url = reverse("user_register")
        data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
            "lastKnowLocLat": 40.0,
            "lastKnowLocLong": 40.0,
            "typesfavEventType": 1,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
