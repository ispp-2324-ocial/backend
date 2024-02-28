from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from base64 import b64encode
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from user.models import OcialClient, OcialUser  
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import OcialClient

from django.contrib.auth import get_user_model

class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True, required=False)
    username = serializers.CharField(write_only=True)

    class Meta:
        model = OcialClient
        fields = ['name', 'identification_document', 'typeClient', 'default_latitude', 'default_longitude', 'password', 'email', 'username']

    def create(self, validated_data):
        # Extract fields for Django user creation
        username = validated_data.pop('username')
        email = validated_data.pop('email', '')
        password = validated_data.pop('password')

        # Create a new User instance
        user = get_user_model().objects.create_user(username=username, email=email, password=password)

        # Create OcialClient instance associated with the created user
        ocial_client = OcialClient.objects.create(**validated_data)

        return ocial_client
        
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Fields:
    - `id` (int): The ID of the user.
    - `username` (string): The username of the user.
    - `email` (string): The email of the user.
    - `password` (string): The password of the user.

    Note:
    - The `password` field is write-only, and it should be sent during user registration.
    """

    class Meta:
        model = OcialUser
        fields = ['usuario']
        extra_kwargs = {'password': {'write_only': True}}

class LoginClientSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Fields:
    - `username` (string): The username of the user.
    - `password` (string): The password of the user.
    """

    model = OcialClient
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
        
class LoginUserSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Fields:
    - `username` (string): The username of the user.
    - `password` (string): The password of the user.
    """

    model = OcialUser
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)