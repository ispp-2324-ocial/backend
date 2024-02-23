from django.shortcuts import render
from rest_framework import generics, status

# Create your views here.
from .models import(
    Event,
    Rating
)

class EventView(generics.ListAPIView):
    def get():
        event_list = Event.objects.all()
        return event_list

class RatingView(generics.ListAPIView):
    def get():
        rating_list = Rating.objects.all()
        return rating_list