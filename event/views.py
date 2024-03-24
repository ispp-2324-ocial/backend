from rest_framework import generics, status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.openapi import OpenApiResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.db.models.functions import ACos, Cos, Radians, Sin
from django.db.models import F
from django.contrib.auth.models import User
import base64
from django.core.files.base import ContentFile
import blurhash
from PIL import Image
from images.models import Image as ImageModel
from user.models import OcialClient, OcialUser
from .models import OcialEventForm, Like, Event
from rest_framework.authtoken.models import Token


# Create your views here.


class EventClientGet(APIView):
    @extend_schema(
        description="Get client instance by event id",
        responses={
            200: OpenApiResponse(response=OcialClientSerializer(many=True)),
            404: OpenApiResponse(response=None, description="Event not found"),
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def get(self, request, *args, **kwargs):
        try:
            event = Event.objects.get(pk=kwargs["pk"])
        except Event.DoesNotExist:
            return Response(
                {"error": "No existe el evento"}, status=status.HTTP_404_NOT_FOUND
            )
        oc = OcialClient.objects.get(pk=event.ocialClient.pk)
        return Response(OcialClientSerializer(oc).data, status=status.HTTP_200_OK)


class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @extend_schema(
        description="List of events",
        responses={
            200: OpenApiResponse(response=EventSerializer(many=True)),
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class EventListByClient(generics.ListAPIView):
    serializer_class = EventSerializer

    @extend_schema(
        description="List of events by client id",
        responses={
            200: OpenApiResponse(response=EventSerializer(many=True)),
            400: OpenApiResponse(response=None, description="No estás logueado"),
        },
    )
    def get(self, request, *args, **kwargs):
        if not User.objects.filter(id=request.user.id).exists():
            return Response(
                {"error": "No estás logueado"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Get list of events if client has events, otherwise []
        try:
            ocialClient = OcialClient.objects.filter(pk=kwargs["pk"])
        except OcialClient.DoesNotExist:
            return Response(
                {"error": "No existe el cliente"}, status=status.HTTP_404_NOT_FOUND
            )
        events = Event.objects.filter(ocialClient=ocialClient[0])
        serialized_events = [EventSerializer(event).data for event in events]
        return Response(serialized_events, status=status.HTTP_200_OK)


class EventCreate(generics.CreateAPIView):
    serializer_class = EventSerializer

    @extend_schema(
        request=EventSerializer,
        description="Create a new event",
        responses={
            201: OpenApiResponse(response=None, description="El evento se ha creado"),
            400: OpenApiResponse(
                response=None, description="El usuario no ha iniciado sesión"
            ),
            403: OpenApiResponse(response=None, description="El usuario no es cliente"),
            422: OpenApiResponse(
                response=None, description="El formulario contiene errores"
            ),
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
        print(user)
        ocialClient = OcialClient.objects.get(djangoUser=user)
        request.data.pop("ocialClient")
        if not ocialClient:
            return Response(
                {"error": "No eres cliente"}, status=status.HTTP_403_FORBIDDEN
            )
        request.data["ocialClient"] = ocialClient.id
        data = request.data

        image = data.get("imageB64")

        eventdata = {
            "name": data.get("name"),
            "place": data.get("place"),
            "description": data.get("description"),
            "date": data.get("date"),
            "hour": data.get("hour"),
            "capacity": data.get("capacity"),
            "category": data.get("category"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "ocialClient": data.get("ocialClient"),
        }
        eventform = OcialEventForm(eventdata)
        if eventform.is_valid():
            eventform.save()
            if image:
                try:
                    image_data = base64.b64decode(image, validate=True)
                except Exception:
                    eventform.instance.delete()
                    return Response(
                        {"error": "Formato de imagen no válido"},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    )
                format, imgstr = image.split(";base64,")
                ext = format.split("/")[-1]
                valid_ext = ["jpg", "jpeg", "png"]
                if ext not in valid_ext:
                    return Response(
                        {"error": "Formato de imagen no válido"},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    )
                imagefile = ContentFile(
                    base64.b64decode(imgstr),
                    name=f"event-{eventform.instance.id}.{ext}",
                )
                image = ImageModel.objects.create(
                    image=imagefile,
                    blurhash=blurhash.encode(
                        Image.open(imagefile), x_components=4, y_components=3
                    ),
                )
                eventform.instance.image = image
                eventform.instance.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"errors": eventform.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )


class EventDelete(generics.DestroyAPIView):

    @extend_schema(
        description="Delete an event",
        responses={
            204: OpenApiResponse(
                response=None, description="El evento se ha eliminado"
            ),
            400: OpenApiResponse(
                response=None, description="El usuario no ha iniciado sesión"
            ),
            403: OpenApiResponse(response=None, description="El usuario no es cliente"),
            404: OpenApiResponse(response=None, description="El evento no existe"),
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
        ocialClient = OcialClient.objects.get(djangoUser=user)
        if not ocialClient:
            return Response(
                {"error": "No eres cliente"}, status=status.HTTP_403_FORBIDDEN
            )
        eventAct = Event.objects.filter(id=kwargs["pk"])
        if not eventAct.exists():
            return Response(
                {"error": "No existe el evento"}, status=status.HTTP_404_NOT_FOUND
            )
        if not (ocialClient.id == eventAct[0].ocialClient.id):
            return Response(
                {"error": "No puedes borrar el evento de otra persona"}, status=status.HTTP_403_FORBIDDEN
            )

        if eventAct.exists():
            eventAct.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)


class EventUpdate(APIView):
    serializer_class = EventSerializer

    @extend_schema(
        request=EventSerializer,
        description="Update an event",
        responses={
            200: OpenApiResponse(
                response=None, description="El evento se ha actualizado"
            ),
            400: OpenApiResponse(
                response=None, description="El usuario no ha iniciado sesión"
            ),
            403: OpenApiResponse(
                response=None, description="El evento no pertenece al usuario activo"
            ),
            422: OpenApiResponse(
                response=None, description="El formulario contiene errores"
            ),
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
        ocialClient = OcialClient.objects.get(djangoUser=user)
        if not ocialClient:
            return Response(
                {"error": "No puedes ed."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            eventAct = Event.objects.get(id=kwargs["pk"])
        except Event.DoesNotExist:
            return Response(
                {"error": "No existe el evento"}, status=status.HTTP_404_NOT_FOUND
            )
        if not (ocialClient.id == eventAct.ocialClient.id):
            return Response(
                {"error": "No puedes actualizar datos de un evento de otro cliente"},
                status=status.HTTP_403_FORBIDDEN,
            )
        request.data["ocialClient"] = ocialClient.id
        data = request.data
        image = data.get("imageB64")
        eventdata = {
            "name": data.get("name"),
            "place": data.get("place"),
            "description": data.get("description"),
            "date": data.get("date"),
            "hour": data.get("hour"),
            "capacity": data.get("capacity"),
            "category": data.get("category"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "ocialClient": data.get("ocialClient"),
        }
        eventform = OcialEventForm(eventdata)
        if eventform.is_valid():
            eventUpdate = Event.objects.filter(id=kwargs["pk"])[0]
            eventUpdate.name = data.get("name")
            eventUpdate.place = data.get("place")
            eventUpdate.description = data.get("description")
            eventUpdate.date = data.get("date")
            eventUpdate.hour = data.get("hour")
            eventUpdate.capacity = data.get("capacity")
            eventUpdate.category = data.get("category")
            eventUpdate.latitude = data.get("latitude")
            eventUpdate.longitude = data.get("longitude")
            eventUpdate.save()
            if image:
                try:
                    image_data = base64.b64decode(image, validate=True)
                except Exception:
                    eventform.instance.delete()
                    return Response(
                        {"error": "Formato de imagen no válido"},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    )
                format, imgstr = data.get("image").split(";base64,")
                ext = format.split("/")[-1]
                valid_ext = ["jpg", "jpeg", "png"]
                if ext not in valid_ext:
                    return Response(
                        {"error": "Formato de imagen no válido"},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    )
                imagefile = ContentFile(
                    base64.b64decode(imgstr),
                    name=f"event-{eventUpdate.instance.id}.{ext}",
                )
                image = ImageModel.objects.create(
                    image=imagefile,
                    blurhash=blurhash.encode(
                        Image.open(imagefile), x_components=4, y_components=3
                    ),
                )
                eventUpdate.instance.image = image
                eventUpdate.instance.save()
            return Response(status=status.HTTP_200_OK)
        return Response(eventform.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


# TODO Rating Methods


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


class RatingCreate(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingCreateSerializer

    @extend_schema(
        request=RatingCreateSerializer,
        description="Create a new rating",
        responses={
            201: OpenApiResponse(response=RatingSerializer()),
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RatingDelete(generics.DestroyAPIView):
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
        return super().delete(request, *args, **kwargs)


class RatingUpdate(generics.UpdateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @extend_schema(
        description="Update an existing rating",
        responses={
            200: OpenApiResponse(response=RatingSerializer()),
            400: OpenApiResponse(response=None, description="Error in request"),
            404: OpenApiResponse(response=None, description="Rating not found"),
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class EventNearby(generics.ListAPIView):
    serializer_class = EventNearbySerializer

    @extend_schema(
        description="List of events near a location",
        parameters=[
            OpenApiParameter(
                name="latitude",
                type=float,
                description="Latitude of the center point",
                required=True,
            ),
            OpenApiParameter(
                name="longitude",
                type=float,
                description="Longitude of the center point",
                required=True,
            ),
            OpenApiParameter(
                name="radius",
                type=float,
                description="Radius in kilometers",
                required=True,
            ),
        ],
        responses={
            200: OpenApiResponse(response=EventSerializer(many=True)),
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        latitude = serializer.validated_data["latitude"]
        longitude = serializer.validated_data["longitude"]
        radius = serializer.validated_data["radius"]

        lat_change = (
            radius / 111.0
        )  # Approximately 111 kilometers per degree of latitude
        lng_change = radius / (111.0 * Cos(Radians(latitude)))

        min_lat = latitude - lat_change
        max_lat = latitude + lat_change
        min_lng = longitude - lng_change
        max_lng = longitude + lng_change

        # Calculate the distance from the center point to each event and filter those within the radius
        events = Event.objects.annotate(
            lat_diff=Radians(F("latitude") - latitude),
            lng_diff=Radians(F("longitude") - longitude),
            distance=6371
            * ACos(
                Cos(Radians(latitude))
                * Cos(Radians(F("latitude")))
                * Cos(Radians(F("longitude")) - Radians(longitude))
                + Sin(Radians(latitude)) * Sin(Radians(F("latitude")))
            ),
        ).filter(
            latitude__gte=min_lat,
            latitude__lte=max_lat,
            longitude__gte=min_lng,
            longitude__lte=max_lng,
            distance__lte=radius,
        )

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventLike(generics.ListAPIView):
    serializer_class = LikeSerializer

    @extend_schema(
        description="Get likes of an event",
        responses={
            200: OpenApiResponse(
                response=LikeSerializer(many=True), description="List of likes"
            ),
            404: OpenApiResponse(response=None, description="Event not found"),
        },
    )
    def get(self, request, *args, **kwargs):
        try:
            event = Event.objects.get(pk=kwargs["pk"])
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        likes = Like.objects.filter(event=event)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Like an event",
        responses={
            201: OpenApiResponse(response=LikeSerializer, description="Event liked"),
            404: OpenApiResponse(response=None, description="Event not found"),
            401: OpenApiResponse(response=None, description="Not authenticated"),
            400: OpenApiResponse(response=None, description="Already liked event"),
        },
    )
    def post(self, request, *args, **kwargs):
        try:
            event = Event.objects.get(pk=kwargs["pk"])
        except Event.DoesNotExist:
            return Response(
                {"error": "El evento no existe."}, status=status.HTTP_404_NOT_FOUND
            )
        token = request.headers.get("Authorization")
        if not token:
            return Response(
                {"error": "No estas autenticado."}, status=status.HTTP_401_UNAUTHORIZED
            )
        token = token.split(" ")[1]
        user = Token.objects.get(key=token).user
        user = OcialUser.objects.get(djangoUser=user)
        if not user:
            return Response(
                {"error": "No puedes dar like al evento."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        like_exist = Like.objects.filter(event=event, user=user)
        if like_exist:
            return Response(
                {"error": "Ya has dado like a este evento."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        like = Like.objects.create(event=event, user=user)
        like.save()
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        description="Unlike an event",
        responses={
            204: OpenApiResponse(response=None, description="Event unliked"),
            404: OpenApiResponse(response=None, description="Event not found"),
            401: OpenApiResponse(response=None, description="Not authenticated"),
            400: OpenApiResponse(response=None, description="Not liked event"),
        },
    )
    def delete(self, request, *args, **kwargs):
        try:
            event = Event.objects.get(pk=kwargs["pk"])
        except Event.DoesNotExist:
            return Response(
                {"error": "El evento no existe."}, status=status.HTTP_404_NOT_FOUND
            )
        token = request.headers.get("Authorization")
        if not token:
            return Response(
                {"error": "No estas autenticado."}, status=status.HTTP_401_UNAUTHORIZED
            )
        token = token.split(" ")[1]
        user = Token.objects.get(key=token).user
        user = OcialUser.objects.get(djangoUser=user)
        if not user:
            return Response(
                {"error": "No puedes dar like al evento."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        like = Like.objects.filter(event=event, user=user)
        if not like:
            return Response(
                {"error": "No has dado like a este evento."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
