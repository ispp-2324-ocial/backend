from rest_framework import serializers
from images.serializers import ImageSerializer
from .models import Event, Rating, OcialClient, Like


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


class EventCreateSerializer(serializers.ModelSerializer):
    ocialClient = OcialClientSerializer()
    imageB64 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Event
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    ocialClient = OcialClientSerializer()
    image = ImageSerializer(read_only=True)

    class Meta:
        model = Event
        fields = "__all__"


class EventNearbySerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    radius = serializers.FloatField()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
