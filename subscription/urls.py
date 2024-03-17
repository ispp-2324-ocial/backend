from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.SubscriptionList.as_view(), name="subscription-list"),
    path("create/", views.SubscriptionListCreateAPIView.as_view(), name="subscription-list-create"),
]