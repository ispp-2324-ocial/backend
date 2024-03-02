from rest_framework import generics

from subscription.models import Subscription


class SubscriptionView(generics.LisTAPIView):
    def get():
        subscription_list = Subscription.objetcs.all()
        return subscription_list
