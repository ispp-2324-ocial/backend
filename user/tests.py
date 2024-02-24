from django.test import TestCase
from .models import OcialUser
from django.contrib.auth.models import User

class OcialUserTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user('ocialuser1', 'chevy@chase.com', 'chevyspassword')
        self.user_2 = User.objects.create_user('ocialuser2', 'chevy@chase.com', 'chevyspassword')
        self.user_3 = User.objects.create_user('ocialuser3', 'chevy@chase.com', 'chevyspassword')
        self.user_4 = User.objects.create_user('ocialuser4', 'chevy@chase.com', 'chevyspassword')

        self.user1 = OcialUser.objects.create(
            usuario = self.user_1,
            city = "Seville",
            dni = "A12345678" #cif
        )
        
        self.user2 = OcialUser.objects.create(
            usuario = self.user_2,
            city = "Seville",
            dni = "12345678A" #nif
        )

        self.user3 = OcialUser.objects.create(
            usuario = self.user_3,
            city = "Seville",
            dni = "X12345678A" #nie
        )

        self.user4 = OcialUser.objects.create(
            usuario = self.user_4,
            city = "Seville",
            #dni nulo
        )

        self.list1 = [self.user1, self.user2, self.user3]
    
    def test_get_users(self):
        self.list2 = [self.user1, self.user2, self.user3]
        self.assertEqual(self.list1, self.list2)