from rest_framework import serializers
from TraineerbookApp.models import *
from rest_framework.serializers import ModelSerializer
from TraineerbookApp.serializer import *
from base64 import b64encode
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from user.models import OcialClient, OcialUser q    

class ClientSerializer(serializers.ModelSerializer):
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
        model = OcialClient
        fields = ['usuario', 'name', 'identification_document', 'typeClient', 'default_latitude', 'default_longitude']
        extra_kwargs = {'password': {'write_only': True}}
        
        
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