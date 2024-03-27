from rest_framework import generics
from rest_framework.views import APIView
from subscription.models import Subscription
from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiResponse
from .models import Subscription
from .serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from user.models import OcialClient
from rest_framework.permissions import IsAuthenticated
from .models import SubscriptionForm


SUBSCRIPTION_DETAILS = {
    "Free": {
        "numEvents": 1,
        "canEditEvent": False,
        "canSendNotifications": False,
        "canHaveRecurrentEvents": False,
        "canHaveOustandingEvents": False,
        "canHaveRating": False,
    },
    "Basic": {
        "numEvents": 10,
        "canEditEvent": True,
        "canSendNotifications": False,
        "canHaveRecurrentEvents": False,
        "canHaveOustandingEvents": False,
        "canHaveRating": False,
    },
    "Pro": {
        "numEvents": 100000,
        "canEditEvent": True,
        "canSendNotifications": True,
        "canHaveRecurrentEvents": True,
        "canHaveOustandingEvents": True,
        "canHaveRating": True,
    },
}


class SubscriptionView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Retrieve the current subscription for the authenticated user.",
        responses={
            200: OpenApiResponse(response=SubscriptionSerializer),
            400: OpenApiResponse(response=None, description="Bad Request"),
            401: OpenApiResponse(response=None, description="Unauthorized"),
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
            subscription = Subscription.objects.get(ocialClientId=ocial_client)
            serialized_subscription = self.get_serializer(subscription)
            return Response(serialized_subscription.data, status=status.HTTP_200_OK)
        except OcialClient.DoesNotExist:
            return Response(
                {"error": "No eres cliente"}, status=status.HTTP_403_FORBIDDEN
            )
        except Subscription.DoesNotExist:
            return Response(
                {"error": "No hay suscripción para este cliente"},
                status=status.HTTP_404_NOT_FOUND,
            )


class SubscriptionCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Create a new subscription with specific behavior based on subscription type.",
        request=SubscriptionCreateUpdateSerializer,
        responses={
            201: OpenApiResponse(response=SubscriptionSerializer),
            400: OpenApiResponse(response=None, description="Bad Request"),
            500: OpenApiResponse(response=None, description="Internal Server Error"),
        },
    )
    def post(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return Response(
                {"error": "No estás autenticado"}, status=status.HTTP_401_UNAUTHORIZED
            )

        type_subscription = request.data.get("typeSubscription")
        if type_subscription not in ["Free", "Basic", "Pro"]:
            return Response(
                {"error": "El parametro typeSubscription debe ser Free, Basic o Pro"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            key = token.split(" ")[1]
            token_obj = Token.objects.get(key=key)
            user = token_obj.user
        except Token.DoesNotExist:
            return Response(
                {"error": "Token inválido"}, status=status.HTTP_401_UNAUTHORIZED
            )

        ocial_client = OcialClient.objects.filter(djangoUser=user).first()
        if not ocial_client:
            return Response(
                {"error": "No eres cliente"}, status=status.HTTP_403_FORBIDDEN
            )

        existing_subscription = Subscription.objects.filter(ocialClientId=ocial_client)
        if existing_subscription.exists():
            return Response(
                {"error": "Ya tienes una suscripción activa"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.data["ocialClientId"] = ocial_client
        data = request.data

        subscription_data = {
            "typeSubscription": type_subscription,
            "numEvents": SUBSCRIPTION_DETAILS[type_subscription]["numEvents"],
            "canEditEvent": SUBSCRIPTION_DETAILS[type_subscription]["canEditEvent"],
            "canSendNotifications": SUBSCRIPTION_DETAILS[type_subscription][
                "canSendNotifications"
            ],
            "canHaveRecurrentEvents": SUBSCRIPTION_DETAILS[type_subscription][
                "canHaveRecurrentEvents"
            ],
            "canHaveOustandingEvents": SUBSCRIPTION_DETAILS[type_subscription][
                "canHaveOustandingEvents"
            ],
            "canHaveRating": SUBSCRIPTION_DETAILS[type_subscription]["canHaveRating"],
            "ocialClientId": data.get("ocialClientId"),
        }

        subscription_form = SubscriptionForm(subscription_data)
        if subscription_form.is_valid():
            subscription_form.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"errors": subscription_form.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


from django.http import JsonResponse


class SubscriptionUpdate(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=SubscriptionCreateUpdateSerializer,
        description="Update the subscription of the authenticated user",
        responses={
            200: OpenApiResponse(response=SubscriptionCreateUpdateSerializer),
            400: OpenApiResponse(description="Bad Request"),
            401: OpenApiResponse(description="Unauthorized"),
            403: OpenApiResponse(description="Forbidden"),
        },
    )
    def put(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return Response(
                {"error": "No estás autenticado"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            key = token.split(" ")[1]
            token_obj = Token.objects.get(key=key)
            user = token_obj.user
        except Token.DoesNotExist:
            return Response(
                {"error": "Token inválido"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if not User.objects.filter(id=user.id).exists():
            return Response(
                {"error": "No estás logueado"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            subscription = Subscription.objects.get(ocialClientId__djangoUser=user)
        except Subscription.DoesNotExist:
            return Response(
                {"error": "No se encontró la suscripción del usuario"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SubscriptionCreateUpdateSerializer(subscription, data=request.data)
        if serializer.is_valid():
            serializer.save()

            type_subscription = serializer.validated_data.get("typeSubscription")
            if type_subscription in SUBSCRIPTION_DETAILS:
                subscription_details = SUBSCRIPTION_DETAILS[type_subscription]
                for key, value in subscription_details.items():
                    setattr(subscription, key, value)
                subscription.save()
            else:
                return JsonResponse(
                    {"error": "Tipo de suscripción no válido"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionDelete(generics.DestroyAPIView):

    @extend_schema(
        description="Delete the current subscription of the authenticated user.",
        responses={
            204: OpenApiResponse(description="Subscription deleted successfully"),
            401: OpenApiResponse(response=None, description="Unauthorized"),
            404: OpenApiResponse(response=None, description="Subscription not found"),
        },
    )
    def delete(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return Response(
                {"error": "No estás autenticado"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            key = token.split(" ")[1]
            token_obj = Token.objects.get(key=key)
            user = token_obj.user
        except Token.DoesNotExist:
            return Response(
                {"error": "Token inválido"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            subscription = Subscription.objects.get(ocialClientId__djangoUser=user)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Subscription.DoesNotExist:
            return Response(
                {"error": "No hay suscripción para este usuario"},
                status=status.HTTP_404_NOT_FOUND,
            )
