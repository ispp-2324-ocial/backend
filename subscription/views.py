from rest_framework import generics

from subscription.models import Subscription


class SubscriptionView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        subscription_list = Subscription.objetcs.all()
        return subscription_list
