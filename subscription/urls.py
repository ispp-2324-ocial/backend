from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.SubscriptionView.as_view(), name='subscription-get'),
    path("create/", views.SubscriptionCreate.as_view(), name="subscription_create"),
    path("delete/", views.SubscriptionDelete.as_view(), name="subscription_delete"),
    path("update/", views.SubscriptionUpdate.as_view(), name="subscription_update"),
]
