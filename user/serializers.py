from rest_framework import serializers
from user.models import OcialClient, OcialUser
from django.contrib.auth.models import User


class DjangoUserSerializer(serializers.ModelSerializer):
    """
    Serializer for djangouser registration.

    Fields:
    - `username` (string): The username of the user.
    - `email` (string): The email of the user.
    - `password` (string): The password of the user.

    Note:
    - The `password` field is write-only, and it should be sent during user registration.
    """

    class Meta:
        model = User
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True, required=False)
    username = serializers.CharField(write_only=True)

    class Meta:
        model = OcialClient
        exclude = ('djangoUser', )


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True, required=False)
    username = serializers.CharField(write_only=True)

    class Meta:
        model = OcialUser
        exclude = ('djangoUser', )


class LoginUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.

    Fields:
    - `username` (string): The username of the user.
    - `password` (string): The password of the user.
    """

    class Meta:
        model = User
        fields = ("username", "password")
