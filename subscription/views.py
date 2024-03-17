from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import OpenApiResponse
from .models import Subscription
from .serializers import SubscriptionSerializer
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

class SubscriptionCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated] 

    @extend_schema(
        description="Create a new subscription with specific behavior based on subscription type.",
        request=SubscriptionSerializer,
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
        request.data["ocialClientId"] = ocialClient.id
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
            subscriptionform.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"errors": subscriptionform.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

