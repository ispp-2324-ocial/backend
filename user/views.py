from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .serializers import *
from .models import OcialClientForm
from .models import OcialUserForm
import random
from django.conf import settings
import base64
from django.core.files.base import ContentFile
import blurhash
from PIL import Image
from images.models import Image as ImageModel
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


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
                response=None, description="El nombre de usuario o correo ya existe"
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

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "El correo ya está registrado"},
                status=status.HTTP_409_CONFLICT,
            )
        
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"error": "El correo es inválido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
                "lastKnowLocLat": request.data.get("lastKnowLocLat"),
                "lastKnowLocLong": request.data.get("lastKnowLocLong"),
                "typesFavEventType": request.data.get("typesFavEventType"),
                "djangoUser": userCreated,
                "auth_provider": "email",
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
                client = OcialClient.objects.filter(djangoUser=user)
                if client:
                    isClient = True
                    client = client[0]
                else:
                    isClient = False
                    client = None
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
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutUserView(APIView):
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
        request=ClientCreateSerializer,
        responses={
            200: OpenApiResponse(response=None),
            400: OpenApiResponse(
                response=None, description="Los datos de la petición son incorrectos"
            ),
            409: OpenApiResponse(
                response=None, description="El nombre de usuario o correo ya existe"
            ),
            422: OpenApiResponse(
                response=None, description="Formato de imagen no válido"
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

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "El correo ya está registrado"},
                status=status.HTTP_409_CONFLICT,
            )

        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"error": "El correo es inválido"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        data = request.data
        image = data.get("imageB64")
        userdata = {
            "username": username,
            "password1": password,
            "password2": password,
            "email": email,
        }
        form = UserCreationForm(userdata)
        if form.is_valid():
            userCreated = form.save()
            ocialclientdata = {
                "name": data.get("name"),
                "identificationDocument": data.get("identificationDocument"),
                "typeClient": data.get("typeClient"),
                "defaultLatitude": data.get("defaultLatitude"),
                "defaultLongitude": data.get("defaultLongitude"),
                "djangoUser": userCreated,
            }
            ocialclientform = OcialClientForm(ocialclientdata)
            if ocialclientform.is_valid():
                samenif = OcialClient.objects.filter(
                    identificationDocument=data.get("identificationDocument")
                )
                if samenif:
                    userCreated.delete()
                    return Response(
                        {
                            "errors": "Este documento de identificación ya se encuentra registrado"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                ocialclientform.save()
                if image:
                    try:
                        image_data = base64.b64decode(
                            image.split(";base64,")[1], validate=True
                        )
                    except Exception:
                        ocialclientform.instance.delete()
                        userCreated.delete()
                        return Response(
                            {"error": "Formato de imagen no es base64 válido"},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        )
                    format, imgstr = image.split(";base64,")
                    ext = format.split("/")[-1]
                    valid_ext = ["jpg", "jpeg", "png"]
                    if ext not in valid_ext:
                        ocialclientform.instance.delete()
                        userCreated.delete()
                        return Response(
                            {"error": "Formato de imagen no válido"},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        )
                    imagefile = ContentFile(
                        base64.b64decode(imgstr),
                        name=f"client-{ocialclientform.instance.id}.{ext}",
                    )
                    image = ImageModel.objects.create(
                        image=imagefile,
                        blurhash=blurhash.encode(
                            Image.open(imagefile), x_components=4, y_components=3
                        ),
                    )
                    ocialclientform.instance.image = image
                    ocialclientform.instance.save()
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


class GoogleSocialAuthView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=GoogleSocialAuthSerializer,
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="GoogleSocialAuthResponse",
                    fields={
                        "token": serializers.StringRelatedField(),
                        "user": "user",
                        "isClient": serializers.BooleanField(),
                        "clientData": "client",
                    },
                ),
                description="Datos del usuario autenticado",
            ),
            400: OpenApiResponse(
                response=None, description="Los datos de la petición son incorrectos"
            ),
        },
    )
    def post(self, request):
        serializer = GoogleSocialAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = (serializer.validated_data)["auth_token"]
        if user_data:
            try:
                user_data["sub"]
            except KeyError:
                return Response(
                    {"error": "Token is not valid."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if user_data["aud"] != settings.GOOGLE_OAUTH2_CLIENT_ID:
                return Response(
                    {"error": "Token is not valid for this app."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            email = user_data.get("email")
            user = User.objects.filter(email=email)
            if user:
                user = user[0]
                ocialuser = OcialUser.objects.filter(usuario=user)
                if ocialuser:
                    ocialuser = ocialuser[0]
                    if ocialuser.auth_provider != "google":
                        return Response(
                            {
                                "error": "User already exists. Try logging in with your email."
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    else:
                        authenticated_user = authenticate(
                            request,
                            username=user.username,
                            password=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                        )
                        token, _ = Token.objects.get_or_create(user=authenticated_user)
                        userdata = DjangoUserSerializer(authenticated_user).data
                        userdata.pop("password")
                        return Response(
                            {
                                "token": token.key,
                                "user": userdata,
                                "isClient": False,
                                "clientData": None,
                            },
                            status=status.HTTP_200_OK,
                        )
            else:
                user = User.objects.create_user(
                    email=email,
                    username=user_data.get("email").split("@")[0]
                    + str(random.randint(0, 1000)),
                    first_name=user_data.get("given_name"),
                    last_name=user_data.get("family_name"),
                    password=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                )
                ocialuserdata = {
                    "usuario": user,
                    "lastKnowLocLat": 0,
                    "lastKnowLocLong": 0,
                    "auth_provider": "google",
                }
                ocialuserform = OcialUserForm(ocialuserdata)
                if ocialuserform.is_valid():
                    ocialuserform.save()
                    authenticated_user = authenticate(
                        request,
                        username=user.username,
                        password=settings.GOOGLE_OAUTH2_CLIENT_SECRET,
                    )
                    token, _ = Token.objects.get_or_create(user=authenticated_user)
                    userdata = DjangoUserSerializer(authenticated_user).data
                    userdata.pop("password")
                    return Response(
                        {
                            "token": token.key,
                            "user": userdata,
                            "isClient": False,
                            "clientData": None,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    user.delete()
                    return Response(
                        {"errors": ocialuserform.errors},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(user_data, status=status.HTTP_200_OK)
        
class RatingList(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @extend_schema(
        description="List of ratings",
        responses={
            200: OpenApiResponse(response=RatingSerializer(many=True)),
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class RatingCreate(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingCreateSerializer

    @extend_schema(
        description="Create a rating",
        responses={
            200: OpenApiResponse(response=RatingCreateSerializer()),
            400: OpenApiResponse(response=None, description="Error in request"),
            404: OpenApiResponse(response=None, description="Rating not found"),
        },
    )
    def post(self, request, *args, **kwargs):

        token = request.headers.get("Authorization")
        if not token:
            return Response(
                {"error": "No estas autenticado."}, status=status.HTTP_401_UNAUTHORIZED
            )
        token = token.split(" ")[1]
        user = Token.objects.get(key=token).user
        # Verify if ocialuser
        try:
            ocial_user = user.ocialuser
        except OcialUser.DoesNotExist:
            return Response({"error": "Solo los usuarios OcialUser pueden crear un rating."},
                            status=status.HTTP_403_FORBIDDEN)

        client = OcialClient.objects.filter(id=kwargs["pk"])
        if not client:
            return Response({"error": "No existe ese cliente."},
                            status=status.HTTP_404_NOT_FOUND)
        
        existing_rating = Rating.objects.filter(client_id=client[0].id, user=ocial_user.djangoUser).exists()
        if existing_rating:
            return Response({"error": "Ya has dado tu opinión sobre este cliente."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Verify Score
        score = request.data.get('score')

        if score > 5:
            score = 5
        
        if score < 0:
            score = 0
        
        # Create rating if all is Ok
        serializer = RatingCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=ocial_user.djangoUser, client = client[0])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RatingIDClientListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer
    
    def get(self, request, *args,**kwargs):
        
        client = OcialClient.objects.filter(id=kwargs["pk"])
        if not client:
            return Response({"error": "No existe ese cliente."},
                            status=status.HTTP_404_NOT_FOUND)
        ratings = Rating.objects.filter(client_id=client[0].id)
        
        serializer = RatingSerializer(ratings, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class RatingDelete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @extend_schema(
        description="Delete a rating",
        responses={
            204: OpenApiResponse(description="Rating deleted successfully"),
            404: OpenApiResponse(response=None, description="Message not found"),
        },
    )
    def delete(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return Response(
                {"error": "No estas autenticado."}, status=status.HTTP_401_UNAUTHORIZED
            )
        token = token.split(" ")[1]
        user = Token.objects.get(key=token).user
            
        # Verificar si el usuario es un OcialUser
        try:
            ocial_user = user.ocialuser
        except OcialUser.DoesNotExist:
            return Response({"error": "No eres un OcialUser."},
                            status=status.HTTP_403_FORBIDDEN)
        
        client = OcialClient.objects.filter(id=kwargs["pk"]).first()
        if not client:
            return Response({"error": "No existe ese cliente."},
                            status=status.HTTP_404_NOT_FOUND)
        
        existing_rating = Rating.objects.filter(client=client, user=ocial_user.djangoUser).first()
        if not existing_rating:
            return Response({"error": "El cliente no tiene un rating tuyo."},
                            status=status.HTTP_400_BAD_REQUEST)
                
        # Eliminar el rating
        existing_rating.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class RatingUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingCreateSerializer

    @extend_schema(
        description="Update an existing rating",
        responses={
            200: OpenApiResponse(response=RatingCreateSerializer()),
            400: OpenApiResponse(response=None, description="Error in request"),
            404: OpenApiResponse(response=None, description="Rating not found"),
        },
    )
    def put(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return Response(
                {"error": "No estas autenticado."}, status=status.HTTP_401_UNAUTHORIZED
            )
        token = token.split(" ")[1]
        user = Token.objects.get(key=token).user
        
        # Verificar si el usuario es un OcialUser
        try:
            ocial_user = user.ocialuser
        except OcialUser.DoesNotExist:
            return Response({"error": "No eres un OcialUser."},
                            status=status.HTTP_403_FORBIDDEN)
        
        client = OcialClient.objects.filter(id=kwargs["pk"]).first()
        if not client:
            return Response({"error": "No existe ese cliente."},
                            status=status.HTTP_404_NOT_FOUND)
        
        existing_rating = Rating.objects.filter(client=client, user=ocial_user.djangoUser).first()
        if not existing_rating:
            return Response({"error": "El cliente no tiene un rating tuyo."},
                            status=status.HTTP_400_BAD_REQUEST)
                
        # Serializando los datos de la solicitud y actualizando el objeto Rating
        serializer = self.get_serializer(existing_rating, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientGetView(generics.ListAPIView):
    serializer_class = ClientGetSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Retrieve the current client data for the authenticated client.",
        responses={
            200: OpenApiResponse(response=ClientGetSerializer),
            400: OpenApiResponse(response=None, description="Bad Request"),
            401: OpenApiResponse(response=None, description="Unauthorized"),
            403: OpenApiResponse(response=None, description="Forbidden"),
        },
    )
    def get(self, request, *args, **kwargs):
        token_key = request.headers.get("Authorization").split(" ")[1]
        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return Response(
                {"error": "Token inválido"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user = token.user
        try:
            ocial_client = OcialClient.objects.get(djangoUser=user)
            serialized_client = self.get_serializer(ocial_client)
            return Response(
                    {
                        "ocialClient": serialized_client.data,
                        "username": user.username,
                        "email": user.email,
                    },
                    status=status.HTTP_200_OK,
                )
        except OcialClient.DoesNotExist:
            return Response(
                {"error": "No eres cliente"}, status=status.HTTP_403_FORBIDDEN
            )
        
class UserGetView(generics.ListAPIView):
    serializer_class = UserGetSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Retrieve the current user data for the authenticated user.",
        responses={
            200: OpenApiResponse(response=UserGetSerializer),
            400: OpenApiResponse(response=None, description="Bad Request"),
            401: OpenApiResponse(response=None, description="Unauthorized"),
            403: OpenApiResponse(response=None, description="Forbidden"),
        },
    )
    def get(self, request, *args, **kwargs):
        token_key = request.headers.get("Authorization").split(" ")[1]
        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            return Response(
                {"error": "Token inválido"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user = token.user
        try:
            ocial_user = OcialUser.objects.get(djangoUser=user)
            serialized_user = self.get_serializer(ocial_user)
            return Response(
                    {
                        "ocialClient": serialized_user.data,
                        "username": user.username,
                        "email": user.email,
                    },
                    status=status.HTTP_200_OK,
                )
        except OcialUser.DoesNotExist:
            return Response(
                {"error": "No eres usuario"}, status=status.HTTP_403_FORBIDDEN
            )
