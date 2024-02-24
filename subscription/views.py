from django.shortcuts import render
from rest_framework import generics, status

from subscription.models import(
    Subscription
)

class SubscriptionView(generics.LisTAPIView):
    def get():
        subscription_list = Subscription.objetcs.all()
        return subscription_list