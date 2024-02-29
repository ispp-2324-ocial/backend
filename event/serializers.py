from rest_framework import serializers
from .models import Event, Rating, OcialClient
from django.contrib.auth.models import User



class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class OcialClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = OcialClient
        fields = '__all__'
        
class EventCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = '__all__'



