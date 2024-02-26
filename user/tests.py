from django.test import TestCase
from .models import OcialUser, OcialClient
from django.contrib.auth.models import User

class OcialUserTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user('ocialuser1', 'chevy@chase.com', 'chevyspassword')
        self.user_2 = User.objects.create_user('ocialuser2', 'chevy@chase.com', 'chevyspassword')
        self.user_3 = User.objects.create_user('ocialuser3', 'chevy@chase.com', 'chevyspassword')
        self.user_4 = User.objects.create_user('ocialuser4', 'chevy@chase.com', 'chevyspassword')

        self.user1 = OcialUser.objects.create(
            usuario = self.user_1,
        )
        
        self.user2 = OcialClient.objects.create(
            usuario = self.user_2,
            name = 'asjodbgfaodvhier',
            identification_document = 'A12345678', #cif
            typeClient = OcialClient.TypeClient.ARTIST,
            default_latitude = 40.7128,
            default_longitude = -40.7128

        )

        self.user3 = OcialClient.objects.create(
            usuario = self.user_3,
            name = 'A',
            identification_document = 'X1234567A', #nie
            typeClient = OcialClient.TypeClient.BAR_RESTAURANT,
            default_latitude = 40.7128,
            default_longitude = 0.0
        )

        self.user4 = OcialClient.objects.create(
            usuario = self.user_4,
            name = 'A',
            identification_document = '12345678A', #dni
            #Default typeClient
            default_latitude = -40.7128,
            default_longitude = 0.0
        )

        self.list1 = [self.user1, self.user2, self.user3, self.user4]
    
    def test_get_users(self):
        self.list2 = [self.user1, self.user2, self.user3, self.user4]
        self.assertEqual(self.list1, self.list2)
        self.assertEqual(self.user4.typeClient, OcialClient.TypeClient.SMALL_BUSINESS)