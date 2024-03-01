from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import generics
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from .serializers import *


class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=UserSerializer,
        responses={
            200: OpenApiResponse(response=None),
            400: OpenApiResponse(response=None, description="Los datos de la petición son incorrectos"),
            409: OpenApiResponse(response=None, description="El nombre de usuario ya existe")
        }
    )
    def post(self, request):
        User = get_user_model()

        serializer = UserSerializer(data=request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({"error": "El nombre de usuario ya existe"}, status=status.HTTP_409_CONFLICT)
        
        user_created = User.objects.create_user(username=username, password=password, email=email)

        data = request.data
        data['usuario'] = user_created.id

        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            data.pop('username')
            data.pop('password')
            data.pop('email')

            # Crear un nuevo OcialUser
            ocial_user = OcialUser.objects.create(
                lastKnowLocLat=data.get('lastKnowLocLat'),
                lastKnowLocLong=data.get('lastKnowLocLong'),
                typesfavEventType=data.get('typesfavEventType'),
                usuario_id=user_created.id
            )

            # Iniciar sesión automáticamente después del registro
            login(request, user_created)

            return Response(status=status.HTTP_200_OK)

        # Verificar específicamente si el error es debido al nombre de usuario duplicado
        if 'username' in serializer.errors and 'Ya existe un usuario con este nombre.' in serializer.errors['username']:
            return Response({"error": "El nombre de usuario ya existe"}, status=status.HTTP_409_CONFLICT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    """
    Inicia la sesión del usuario y devuelve el token de autenticación
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LoginUserSerializer,
        responses={
            200: OpenApiResponse(response=inline_serializer(
                    name='TokenResponse',
                    fields={ 'token': serializers.StringRelatedField() }),
                description="Token de autenticación"),
            400: OpenApiResponse(response=None, description="Los datos de la petición son incorrectos"),
            401: OpenApiResponse(response=None, description="Las credenciales son incorrectas")}
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        serializer = LoginUserSerializer(data=user)
        if serializer:
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)

                # Inicia sesión al usuario autenticado
                login(request, user)

                return Response({'token': token.key }, status=status.HTTP_200_OK)
            else:
                # La contraseña es incorrecta o no existe el usuario
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutUserView(APIView):
    """
    Cierra la sesión del usuario 
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(response=None),
            304: OpenApiResponse(response=None, description="Django ha detectado un usuario, pero el token no existe, por lo que se considera que la sesión está cerrada"),
            401: OpenApiResponse(response=None, description="El usuario no está autenticado")}
    )
    def post(self, request):
        # Obtener el token asociado al usuario actual
        try:
            token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            # Si el token no existe, la sesión ya se considera cerrada
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        # Eliminar el token de autenticación
        token.delete()

        return Response(status=status.HTTP_200_OK)
    
class RegisterClientView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=ClientSerializer,
        responses={
            200: OpenApiResponse(response=None),
            400: OpenApiResponse(response=None, description="Los datos de la petición son incorrectos"),
            409: OpenApiResponse(response=None, description="El nombre de usuario ya existe")
        }
    )
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if User.objects.filter(username=username).exists():
            return Response({"error": "El nombre de usuario ya existe"}, status=status.HTTP_409_CONFLICT)
        
        userCreated = get_user_model().objects.create_user(username= username, password = password, email=email)
        userCreated.set_password(request.data.get('password'))
        userCreated.save()

        data = request.data
        data['usuario'] = userCreated.id

        serializer = ClientSerializer(data=data)

        if serializer.is_valid():            
            # Verificar si el nombre de usuario ya existe
            data.pop('username')
            data.pop('password')
            data.pop('email')


            ocial_client = OcialClient.objects.create(name=data.get('name'), identification_document=data.get('identification_document'), typeClient=data.get('typeClient'),
            default_latitude=data.get('default_latitude'), default_longitude=data.get('default_longitude'), usuario= userCreated)

            user_instance = User.objects.get(pk=userCreated.id)
            ocial_client.usuario = user_instance
            ocial_client.save()

            # Iniciar sesión automáticamente después del registro
            login(request, userCreated)

            return Response(status=status.HTTP_200_OK)

        # Verificar específicamente si el error es debido al nombre de usuario duplicado
        if 'username' in serializer.errors and 'Ya existe un usuario con este nombre.' in serializer.errors['username']:
            return Response({"error": "El nombre de usuario ya existe"}, status=status.HTTP_409_CONFLICT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)