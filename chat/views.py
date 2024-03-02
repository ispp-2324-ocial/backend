from rest_framework import generics
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiResponse
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, MessageCreateSerializer
from rest_framework.response import Response


class ChatList(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    @extend_schema(
        description="List of chats",
        responses={
            200: OpenApiResponse(response=ChatSerializer(many=True)),
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ChatDetail(generics.RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    @extend_schema(
        description="Detail of a chat",
        responses={
            200: OpenApiResponse(response=ChatSerializer()),
            404: OpenApiResponse(response=None, description="Chat not found"),
        },
    )
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        messages = Message.objects.filter(chat=instance)
        sorted_messages = sorted(
            messages, key=lambda message: message.id
        )  # Ordenar por ID
        message_data = [
            f"{message.id}: {message.content}" for message in sorted_messages
        ]
        data = serializer.data
        data["messages"] = message_data
        return Response(data)


class MessageCreate(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageCreateSerializer

    @extend_schema(
        request=MessageCreateSerializer,
        description="Create a new message in a chat",
        responses={
            201: OpenApiResponse(response=MessageSerializer()),
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MessageDelete(generics.DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @extend_schema(
        description="Delete a message",
        responses={
            204: OpenApiResponse(description="Message deleted successfully"),
            404: OpenApiResponse(response=None, description="Message not found"),
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ChatDelete(generics.DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    @extend_schema(
        description="Delete a chat",
        responses={
            204: OpenApiResponse(description="Chat deleted successfully"),
            404: OpenApiResponse(response=None, description="Chat not found"),
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ChatCreate(generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    @extend_schema(
        request=ChatSerializer,
        description="Create a new chat",
        responses={
            201: OpenApiResponse(response=ChatSerializer()),
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
