from django.shortcuts import render
from rest_framework import generics, status

# Create your views here.
from .models import(
    Rating
)

class RatingView(generics.ListAPIView):
    def get():
        rating_list = Rating.objects.all()
        return rating_list