from rest_framework import serializers
from .models import Subscription

class SubscriptionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['typeSubscription']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"