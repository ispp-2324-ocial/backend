from django.shortcuts import render
# Create your views here.
from rest_framework import viewsets

from .models import Notification, OcialNotificationForm
from .serializers import NotificationCreateSerializer, NotificationSerializer
from rest_framework import generics, status, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.openapi import OpenApiResponse
from rest_framework.response import Response
from django.contrib.auth.models import User
from user.models import OcialClient


class NotificationViewSet(viewsets.ModelViewSet):

    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()


def index(request):
    return render(request, "notification/index.html")


class NotificationCreate(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    serializer_class = NotificationCreateSerializer

    @extend_schema(
        description="Create a notification",
        request=NotificationSerializer,
        responses={
            200: OpenApiResponse(response=NotificationSerializer(many=True)),
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def post(self, request, *args, **kwargs):
        if not User.objects.filter(id=request.user.id).exists():
            return Response(
                {"error": "No estás logueado"}, status=status.HTTP_400_BAD_REQUEST
            )

        ocialClient = OcialClient.objects.filter(usuario=request.user)
        if not ocialClient:
            return Response(
                {"error": "No eres cliente"}, status=status.HTTP_403_FORBIDDEN
            )
        ocialClient = ocialClient[0]
        request.data["ocialClient"] = ocialClient.id
        data = request.data

        notificationdata = {
            "title": data.get("title"),
            "content": data.get("content"),
            "author": data.get("ocialClient"),
            "status": 0,
        }

        notificationform = OcialNotificationForm(notificationdata)
        if notificationform.is_valid():
            notificationform.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"errors": notificationform.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

class NotificationUpdate(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]

    serializer_class = NotificationCreateSerializer

    @extend_schema(
        request=NotificationSerializer,
        description="Update an notification",
        responses={
            201: OpenApiResponse(response=None),
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def put(self, request, *args, **kwargs):
        if not User.objects.filter(id=request.user.id).exists():
            return Response(
                {"error": "No estás logueado"}, status=status.HTTP_400_BAD_REQUEST
            )

        ocialClient = OcialClient.objects.filter(usuario=request.user)
        notificationAct = Notification.objects.filter(id=kwargs["pk"])
        if not ocialClient:
            return Response(
                {"error": "No eres cliente"}, status=status.HTTP_403_FORBIDDEN
            )
        if not notificationAct:
            return Response(
                {"error": "No existe ese id"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not (ocialClient[0].id == notificationAct[0].author.id):
            return Response(
                {"error": "No eres el cliente que ha creado la notificación"}, status=status.HTTP_403_FORBIDDEN
            )
        ocialClient = ocialClient[0]
        request.data["ocialClient"] = ocialClient.id
        data = request.data

        notificationdata = {
            "title": data.get("title"),
            "content": data.get("content"),
            "author": data.get("ocialClient"),
            "status": 0,
        }
        notificationform = OcialNotificationForm(notificationdata)
        if notificationform.is_valid():
            notificationUpdate = Notification.objects.filter(id=kwargs["pk"])[0]
            notificationUpdate.title = data.get("title")
            notificationUpdate.content = data.get("content")
            notificationUpdate.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"errors": notificationform.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

class NotificationDelete(generics.DestroyAPIView):
    @extend_schema(
        description="Delete an notification",
        responses={
            204: OpenApiResponse(description="Notification deleted successfully"),
            404: OpenApiResponse(response=None, description="Notification not found"),
        },
    )
    def delete(self, request, *args, **kwargs):

        if not User.objects.filter(id=request.user.id).exists():
            return Response(
                {"error": "No estás logueado"}, status=status.HTTP_400_BAD_REQUEST
            )

        ocialClient = OcialClient.objects.filter(usuario=request.user)
        notificationAct = Notification.objects.filter(id=kwargs["pk"])
        if not ocialClient:
            return Response(
                {"error": "No eres cliente"}, status=status.HTTP_403_FORBIDDEN
            )
        if not notificationAct:
            return Response(
                {"error": "No existe ese id"}, status=status.HTTP_400_BAD_REQUEST
            )
        print(notificationAct)
        if not (ocialClient[0].id == notificationAct[0].author.id):
            return Response(
                {"error": "No eres el cliente que ha creado la notificación"}, status=status.HTTP_403_FORBIDDEN
            )

        if notificationAct.exists():
            notificationAct.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)

