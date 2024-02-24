from django.test import TestCase
from subscription.models import Subscription

class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.s1 = Subscription.objetcs.create(
            typeSubscription = Subscription.TypeSubscription.FREE
        )
        self.s2 = Subscription.objetcs.create(
            typeSubscription = Subscription.TypeSubscription.BASIC
        )
        self.s2 = Subscription.objetcs.create(
            typeSubscription = Subscription.TypeSubscription.PRO
        )

        self.list1 = [self.e1, self.e2, self.e3]

    def test_get_subscriptions(self):
        self.list2 = [self.s1, self.s2, self.s3]
        self.assertEquals(self.list1,self.list2)
