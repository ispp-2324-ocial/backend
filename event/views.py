from django.shortcuts import render
from rest_framework import generics, status
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiResponse 
from rest_framework.response import Response
from .serializers import *

# Create your views here.
from .models import(
    Event,
    Rating
)

class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @extend_schema(
        description="List of events",
        responses={
            200: OpenApiResponse(response=EventSerializer(many=True)),
            400: OpenApiResponse(response=None, description="Error in request")
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class EventCreate(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer

    @extend_schema(
        request=EventCreateSerializer,
        description="Create a new event",
        responses={
            201: OpenApiResponse(response=EventSerializer()),
            400: OpenApiResponse(response=None, description="Error in request")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class EventDelete(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @extend_schema(
        description="Delete an event",
        responses={
            204: OpenApiResponse(description="Event deleted successfully"),
            404: OpenApiResponse(response=None, description="Message not found")
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
class EventUpdate(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @extend_schema(
        description="Update an existing event",
        responses={
            200: OpenApiResponse(response=EventSerializer()),
            400: OpenApiResponse(response=None, description="Error in request"),
            404: OpenApiResponse(response=None, description="Event not found"),
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

class RatingList(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @extend_schema(
        description="List of ratings",
        responses={
            200: OpenApiResponse(response=RatingSerializer(many=True)),
            400: OpenApiResponse(response=None, description="Error in request")
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class RatingCreate(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingCreateSerializer

    @extend_schema(
        request= RatingCreateSerializer,
        description="Create a new rating",
        responses={
            201: OpenApiResponse(response=RatingSerializer()),
            400: OpenApiResponse(response=None, description="Error in request")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class RatingDelete(generics.DestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @extend_schema(
        description="Delete a rating",
        responses={
            204: OpenApiResponse(description="Rating deleted successfully"),
            404: OpenApiResponse(response=None, description="Message not found")
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
class RatingUpdate(generics.UpdateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @extend_schema(
        description="Update an existing rating",
        responses={
            200: OpenApiResponse(response=RatingSerializer()),
            400: OpenApiResponse(response=None, description="Error in request"),
            404: OpenApiResponse(response=None, description="Rating not found"),
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    