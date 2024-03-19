from rest_framework import serializers
from user.models import OcialClient, OcialUser
from django.contrib.auth.models import User
from . import google
from django.conf import settings


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
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True, required=False)
    username = serializers.CharField(write_only=True)

    class Meta:
        model = OcialUser
        fields = "__all__"


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


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data["sub"]
        except KeyError:
            raise serializers.ValidationError(
                "The token is invalid or expired. Please login again."
            )

        if user_data["aud"] != settings.GOOGLE_OAUTH2_CLIENT_ID:
            raise serializers.ValidationError("Token is not valid for this app.")
        return user_data
