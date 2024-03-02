from rest_framework import generics, status, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.openapi import OpenApiResponse
from rest_framework.response import Response
from .serializers import *
from django.db.models.functions import ACos, Cos, Radians, Sin
from django.db.models import F


# Create your views here.
from .models import Event, Rating


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
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def get(self, request, *args, **kwargs):
        if not User.objects.filter(id=request.user.id).exists():
            return Response(
                {"error": "No estás logueado"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Get list of events if client has events, otherwise []
        ocialClient = OcialClient.objects.filter(usuario=kwargs["pk"])
        if ocialClient:
            events = Event.objects.filter(ocialClient=ocialClient[0].id)
            serialized_events = [EventSerializer(event).data for event in events]
            return Response(serialized_events, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)


class EventCreate(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=EventSerializer,
        description="Create a new event",
        responses={
            201: OpenApiResponse(response=None),
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def post(self, request, *args, **kwargs):
        if not User.objects.filter(id=request.user.id).exists():
            return Response(
                {"error": "No estás logueado"}, status=status.HTTP_400_BAD_REQUEST
            )

        request.data.pop("ocialClient")
        ocialClient = OcialClient.objects.filter(usuario=request.user)
        if not ocialClient:
            return Response(
                {"error": "No eres cliente"}, status=status.HTTP_403_FORBIDDEN
            )
        ocialClient = ocialClient[0]
        request.data["ocialClient"] = ocialClient.id
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            name = request.data.get("name")
            place = request.data.get("place")
            event = request.data.get("event")
            date = request.data.get("date")
            hour = request.data.get("hour")
            capacity = request.data.get("capacity")
            category = request.data.get("category")
            latitude = request.data.get("latitude")
            longitude = request.data.get("longitude")
            eventCreated = Event.objects.create(
                name=name,
                place=place,
                event=event,
                date=date,
                hour=hour,
                capacity=capacity,
                category=category,
                latitude=latitude,
                longitude=longitude,
                ocialClient=ocialClient,
            )
            eventCreated.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDelete(generics.DestroyAPIView):

    @extend_schema(
        description="Delete an event",
        responses={
            204: OpenApiResponse(description="Event deleted successfully"),
            404: OpenApiResponse(response=None, description="Message not found"),
        },
    )
    def delete(self, request, *args, **kwargs):

        if not User.objects.filter(id=request.user.id).exists():
            return Response(
                {"error": "No estás logueado"}, status=status.HTTP_400_BAD_REQUEST
            )

        ocialClient = OcialClient.objects.filter(usuario=request.user)
        eventAct = Event.objects.filter(id=kwargs["pk"])
        if not (ocialClient[0].id == eventAct[0].ocialClient.id):
            return Response(
                {"error": "No eres cliente"}, status=status.HTTP_403_FORBIDDEN
            )

        if eventAct.exists():
            eventAct.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class EventUpdate(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EventSerializer

    @extend_schema(
        request=EventSerializer,
        description="Update an event",
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

        request.data.pop("ocialClient")
        ocialClient = OcialClient.objects.filter(usuario=request.user)
        eventAct = Event.objects.filter(id=kwargs["pk"])
        if not (ocialClient[0].id == eventAct[0].ocialClient.id):
            return Response(
                {"error": "No eres cliente"}, status=status.HTTP_403_FORBIDDEN
            )
        ocialClient = ocialClient[0]
        request.data["ocialClient"] = ocialClient.id
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            eventUpdate = Event.objects.filter(id=kwargs["pk"])[0]
            eventUpdate.name = request.data.get("name")
            eventUpdate.place = request.data.get("place")
            eventUpdate.event = request.data.get("event")
            eventUpdate.date = request.data.get("date")
            eventUpdate.hour = request.data.get("hour")
            eventUpdate.capacity = request.data.get("capacity")
            eventUpdate.category = request.data.get("category")
            eventUpdate.latitude = request.data.get("latitude")
            eventUpdate.longitude = request.data.get("longitude")
            eventUpdate.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


from drf_spectacular.utils import OpenApiParameter


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
