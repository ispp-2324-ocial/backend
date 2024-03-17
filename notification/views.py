from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):

    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()


def index(request):
    return render(request, "notification/index.html")

