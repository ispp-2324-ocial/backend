from django.test import TestCase
from event.models import Rating

# Create your tests here.

class RatingTestCase(TestCase):
    def setUp(self):
        self.r1 = Rating.objects.create(
            score = 3,
            comment = 'Esto es un test'
        )
        
        self.r2 = Rating.objects.create(
            score = 2,
            comment = ''
        )

        self.list1 = [self.r1, self.r2]
    
    def test_get_rating(self):
        self.list2 = [self.r1, self.r2]
        self.assertEqual(self.list1, self.list2)