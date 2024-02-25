from rest_framework import serializers
from .models import Event, Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'

class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        
class EventCreateSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = '__all__'

