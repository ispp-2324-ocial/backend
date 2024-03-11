from rest_framework import serializers
from .models import Event, Rating, OcialClient


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"


class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"


class OcialClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = OcialClient
        fields = ["name", "defaultLatitude", "defaultLongitude"]


class EventSerializer(serializers.ModelSerializer):
    ocialClient = OcialClientSerializer()

    class Meta:
        model = Event
        fields = "__all__"


class EventNearbySerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    radius = serializers.FloatField()
