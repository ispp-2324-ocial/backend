from rest_framework import generics, status, permissions
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiResponse
from .models import Subscription
from .serializers import *
from django.contrib.auth.models import User
from user.models import OcialClient
from rest_framework.permissions import IsAuthenticated
from .models import SubscriptionForm


class SubscriptionList(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @extend_schema(
        description="List of subscriptions",
        responses={
            200: OpenApiResponse(response=SubscriptionSerializer(many=True)),
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class SubscriptionListByClient(generics.ListAPIView):
    serializer_class = SubscriptionSerializer

    @extend_schema(
        description="Subscription by client id",
        responses={
            200: OpenApiResponse(response=SubscriptionSerializer(many=True)),
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def get(self, request, *args, **kwargs):
        if not User.objects.filter(id=request.user.id).exists():
            return Response(
                {"error": "No estás logueado"}, status=status.HTTP_400_BAD_REQUEST
            )
        # Get list of subscription if client has subscription, otherwise []
        ocialClient = OcialClient.objects.filter(usuario=kwargs["pk"])
        if ocialClient:
            suscripciones = Subscription.objects.filter(ocialClientId=ocialClient[0].id)
            serialized_subscription = [SubscriptionSerializer(suscripcion).data for suscripcion in suscripciones]
            return Response(serialized_subscription, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)

class SubscriptionCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated] 

    @extend_schema(
        description="Create a new subscription with specific behavior based on subscription type.",
        request=SubscriptionCreateUpdateSerializer,
        responses={
            201: OpenApiResponse(response=SubscriptionSerializer),
            400: OpenApiResponse(response=None, description="Bad Request"),
            500: OpenApiResponse(response=None, description="Internal Server Error"),
        }
    )
    def post(self, request, *args, **kwargs):
        type_subscription = request.data.get('typeSubscription') 
        if type_subscription not in ['Free', 'Basic', 'Pro']:  
            return Response({"error": "El parametro typeSubscription debe ser Free, Basic o Pro"}, status=status.HTTP_400_BAD_REQUEST)
        
        ocialClient = OcialClient.objects.filter(usuario=request.user)
        if not ocialClient:
            return Response(
                {"error": "No eres cliente"}, status=status.HTTP_403_FORBIDDEN
            )
        ocialClient = ocialClient[0]
        request.data["ocialClientId"] = ocialClient
        data = request.data

        existsubscription = Subscription.objects.filter(ocialClientId=ocialClient.id)
        if existsubscription:
            return Response(
                {"error": "Este cliente ya tiene una suscripcion"}, status=status.HTTP_403_FORBIDDEN
            )

        subscription_data = {}
        if type_subscription == 'Free':
            subscription_data = {
                'typeSubscription': 'Free',
                'numEvents': 1,
                'canEditEvent': False,
                'canSendNotifications': False,
                'canHaveRecurrentEvents': False,
                'canHaveOustandingEvents': False,
                'canHaveRating': False,
                "ocialClientId": data.get("ocialClientId"),
            }
        elif type_subscription == 'Basic':
            subscription_data = {
                'typeSubscription': 'Basic',
                'numEvents': 10,
                'canEditEvent': True,
                'canSendNotifications': False,
                'canHaveRecurrentEvents': False,
                'canHaveOustandingEvents': False,
                'canHaveRating': False,
                "ocialClientId": data.get("ocialClientId"),
            }
        elif type_subscription == 'Pro':
            subscription_data = {
                'typeSubscription': 'Pro',
                'numEvents': 100000,
                'canEditEvent': True,
                'canSendNotifications': True,
                'canHaveRecurrentEvents': True,
                'canHaveOustandingEvents': True,
                'canHaveRating': True,
                "ocialClientId": data.get("ocialClientId"),
            }

        subscriptionform = SubscriptionForm(subscription_data)
        if subscriptionform.is_valid():
            subscriptionform.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"errors": subscriptionform.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

class SubscriptionDelete(generics.DestroyAPIView):

    @extend_schema(
        description="Delete a subscription",
        responses={
            204: OpenApiResponse(description="Subscription deleted successfully"),
            404: OpenApiResponse(response=None, description="Message not found"),
        },
    )
    def delete(self, request, *args, **kwargs):

        if not User.objects.filter(id=request.user.id).exists():
            return Response(
                {"error": "No estás logueado"}, status=status.HTTP_400_BAD_REQUEST
            )

        ocialClient = OcialClient.objects.filter(usuario=request.user)
        subscriptionAct = Subscription.objects.filter(id=kwargs["pk"])
        if not (ocialClient[0].id == subscriptionAct[0].ocialClientId.id):
            return Response(
                {"error": "No eres cliente"}, status=status.HTTP_403_FORBIDDEN
            )
        if subscriptionAct.exists():
            subscriptionAct.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)

class SubscriptionUpdate(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=SubscriptionCreateUpdateSerializer,
        description="Update an subscription",
        responses={
            201: OpenApiResponse(response=None),
            400: OpenApiResponse(response=None, description="Error in request"),
        },
    )
    def put(self, request, *args, **kwargs):
        type_subscription = request.data.get('typeSubscription') 
        if type_subscription not in ['Free', 'Basic', 'Pro']:  
            return Response({"error": "El parametro typeSubscription debe ser Free, Basic o Pro"}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(id=request.user.id).exists():
            return Response(
                {"error": "No estás logueado"}, status=status.HTTP_400_BAD_REQUEST
            )

        ocialClient = OcialClient.objects.filter(usuario=request.user)
        subscriptionAct = Subscription.objects.filter(id=kwargs["pk"])
        if not (ocialClient[0].id == subscriptionAct[0].ocialClientId.id):
            return Response(
                {"error": "No puedes actualizar datos de un evento de otro cliente"},
                status=status.HTTP_403_FORBIDDEN,
            )
        ocialClient = ocialClient[0]
        request.data["ocialClientId"] = ocialClient
        data = request.data

        subscription_data = {}
        if type_subscription == 'Free':
            subscription_data = {
                'typeSubscription': 'Free',
                'numEvents': 1,
                'canEditEvent': False,
                'canSendNotifications': False,
                'canHaveRecurrentEvents': False,
                'canHaveOustandingEvents': False,
                'canHaveRating': False,
                "ocialClientId": data.get("ocialClientId"),
            }
        elif type_subscription == 'Basic':
            subscription_data = {
                'typeSubscription': 'Basic',
                'numEvents': 10,
                'canEditEvent': True,
                'canSendNotifications': False,
                'canHaveRecurrentEvents': False,
                'canHaveOustandingEvents': False,
                'canHaveRating': False,
                "ocialClientId": data.get("ocialClientId"),
            }
        elif type_subscription == 'Pro':
            subscription_data = {
                'typeSubscription': 'Pro',
                'numEvents': 100000,
                'canEditEvent': True,
                'canSendNotifications': True,
                'canHaveRecurrentEvents': True,
                'canHaveOustandingEvents': True,
                'canHaveRating': True,
                "ocialClientId": data.get("ocialClientId"),
            }
        subscriptionform = SubscriptionForm(subscription_data)
        if subscriptionform.is_valid():
            subscriptionUpdate = Subscription.objects.filter(id=kwargs["pk"])[0]
            subscriptionUpdate.typeSubscription = subscription_data["typeSubscription"]        
            subscriptionUpdate.numEvents = subscription_data['numEvents']
            subscriptionUpdate.canEditEvent = subscription_data["canEditEvent"]
            subscriptionUpdate.canSendNotifications = subscription_data["canSendNotifications"]
            subscriptionUpdate.canHaveRecurrentEvents = subscription_data["canHaveRecurrentEvents"]
            subscriptionUpdate.canHaveOustandingEvents = subscription_data["canHaveOustandingEvents"]
            subscriptionUpdate.canHaveRating = subscription_data["canHaveRating"]
            subscriptionUpdate.ocialClientId = subscription_data["ocialClientId"]
            subscriptionUpdate.save()
            return Response(status=status.HTTP_200_OK)
        return Response(subscriptionform.errors, status=status.HTTP_400_BAD_REQUEST)
