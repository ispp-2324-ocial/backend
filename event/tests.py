from django.test import TestCase
from event.models import Event, Rating

# Create your tests here.

class EventTestCase(TestCase):
    def setUp(self):
        self.e1 = Event.objects.create(
            name="Football Match",
            place="Stadium ABC",
            event="Match between Team A and Team B",
            date="2024-02-25",
            hour="15:00:00",
            capacity=50000,
            category=Event.Category.SPORTS,
            latitude=40.7128,
            longitude=-74.0060
        )
        self.e2 = Event.objects.create(
            name="Music Festival",
            place="Park XYZ",
            event="Annual Music Festival",
            date="2024-07-15",
            hour="18:00:00",
            capacity=10000,
            category=Event.Category.MUSIC,
            latitude=34.0522,
            longitude=-118.2437
        )

        self.list1 = [self.e1, self.e2]
    
    def test_get_events(self):
        self.list2 = [self.e1, self.e2]
        self.assertEqual(self.list1, self.list2)

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
    
    def test_get_ratings(self):
        self.list2 = [self.r1, self.r2]
        self.assertEqual(self.list1, self.list2)