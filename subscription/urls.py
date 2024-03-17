from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.SubscriptionList.as_view(), name="subscription-list"),
    path("create/", views.SubscriptionCreateAPIView.as_view(), name="subscription-create"),
]