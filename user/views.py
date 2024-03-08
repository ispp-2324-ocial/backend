from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .serializers import *
from .models import OcialClientForm
from .models import OcialUserForm


class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=UserSerializer,
        responses={
            200: OpenApiResponse(response=None),
            400: OpenApiResponse(
                response=None, description="Los datos de la petición son incorrectos"
            ),
            409: OpenApiResponse(
                response=None, description="El nombre de usuario ya existe"
            ),
        },
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "El nombre de usuario ya existe"},
                status=status.HTTP_409_CONFLICT,
            )

        data = request.data
        userdata = {
            "username": username,
            "password1": password,
            "password2": password,
            "email": email,
        }
        form = UserCreationForm(userdata)
        if form.is_valid():
            userCreated = form.save()
            ocialuserdata = {
                "lastKnowLocLat": data.get("lastKnowLocLat"),
                "lastKnowLocLong": data.get("lastKnowLocLong"),
                "typesfavEventType": data.get("typesfavEventType"),
                "usuario": userCreated,
            }
            ocialuserform = OcialUserForm(ocialuserdata)
            if ocialuserform.is_valid():
                ocialuserform.save()
                return Response(status=status.HTTP_200_OK)
            else:
                userCreated.delete()
                return Response(
                    {"errors": ocialuserform.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            return Response(
                {"errors": form.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginUserView(APIView):
    """
    Inicia la sesión del usuario y devuelve el token de autenticación
    """

    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LoginUserSerializer,
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="TokenResponse",
                    fields={
                        "token": serializers.StringRelatedField(),
                        "user": "user",
                        "isClient": serializers.BooleanField(),
                        "clientData": "client",
                    },
                ),
                description="Token de autenticación",
            ),
            400: OpenApiResponse(
                response=None, description="Los datos de la petición son incorrectos"
            ),
            401: OpenApiResponse(
                response=None, description="Las credenciales son incorrectas"
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        serializer = LoginUserSerializer(data=user)
        if serializer:
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                client = OcialClient.objects.filter(usuario=user)
                if client:
                    isClient = True
                    client = client[0]
                else:
                    isClient = False
                    client = None
                # Inicia sesión al usuario autenticado
                login(request, user)
                userdata = DjangoUserSerializer(user).data
                userdata.pop("password")
                clientdata = ClientSerializer(client).data
                return Response(
                    {
                        "token": token.key,
                        "user": userdata,
                        "isClient": isClient,
                        "clientData": clientdata,
                    },
                    status=status.HTTP_200_OK,
                )
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
            304: OpenApiResponse(
                response=None,
                description="Django ha detectado un usuario, pero el token no existe, por lo que se considera que la sesión está cerrada",
            ),
            401: OpenApiResponse(
                response=None, description="El usuario no está autenticado"
            ),
        },
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
        logout(request)

        return Response(status=status.HTTP_200_OK)


class RegisterClientView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=ClientSerializer,
        responses={
            200: OpenApiResponse(response=None),
            400: OpenApiResponse(
                response=None, description="Los datos de la petición son incorrectos"
            ),
            409: OpenApiResponse(
                response=None, description="El nombre de usuario ya existe"
            ),
        },
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "El nombre de usuario ya existe"},
                status=status.HTTP_409_CONFLICT,
            )

        data = request.data
        userdata = {
            "username": username,
            "password1": password,
            "password2": password,
            "email": email,
        }
        form = UserCreationForm(userdata)
        if form.is_valid():
            userCreated = form.save()
            dni = data.get("identification_document")
            dni = dni[:-1] + dni[-1].upper()
            ocialclientdata = {
                "name": data.get("name"),
                "identification_document": dni,
                "typeClient": data.get("typeClient"),
                "default_latitude": data.get("default_latitude"),
                "default_longitude": data.get("default_longitude"),
                "usuario": userCreated,
            }
            ocialclientform = OcialClientForm(ocialclientdata)
            if ocialclientform.is_valid():
                samenif = OcialClient.objects.filter(
                    identification_document=data.get("identification_document")
                )
                if samenif:
                    return Response(
                        {
                            "errors": "Este documento de identificación ya se encuentra registrado"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                ocialclientform.save()
                return Response(status=status.HTTP_200_OK)
            else:
                userCreated.delete()
                return Response(
                    {"errors": ocialclientform.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            return Response(
                {"errors": form.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
