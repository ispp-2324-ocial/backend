from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.EventList.as_view(), name="event_list"),
    path("list/client/<int:pk>/", views.EventListByClient.as_view(), name="event_list_by_client"),
    path("create/", views.EventCreate.as_view(), name="event_create"),
    path("<int:pk>/update/", views.EventUpdate.as_view(), name="event_update"),
    path("<int:pk>/delete/", views.EventDelete.as_view(), name="event_delete"),
    path("nearby/", views.EventNearby.as_view(), name="event_nearby"),
    path("rating/list/", views.RatingList.as_view(), name="rating_list"),
    path("rating/create/", views.RatingCreate.as_view(), name="rating_create"),
    path("rating/<int:pk>/update/", views.RatingUpdate.as_view(), name="rating_update"),
    path("rating/<int:pk>/delete/", views.RatingDelete.as_view(), name="rating_delete"),
]
