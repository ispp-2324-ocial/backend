from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.SubscriptionList.as_view(), name="subscription_list"),
    path("list/<int:pk>/", views.SubscriptionListByClient.as_view(), name="subscription_list_by_client"),
    path("create/", views.SubscriptionCreate.as_view(), name="subscription_create"),
    path("<int:pk>/delete/", views.SubscriptionDelete.as_view(), name="subscription_delete"),
    path("<int:pk>/update/", views.SubscriptionUpdate.as_view(), name="subscription_update"),
]