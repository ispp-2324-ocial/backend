from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/client/", views.EventClientGet.as_view(), name="client_get"),
    path("list/", views.EventList.as_view(), name="event_list"),
    path(
        "list/client/<int:pk>/",
        views.EventListByClient.as_view(),
        name="event_list_by_client",
    ),
    path("create/", views.EventCreate.as_view(), name="event_create"),
    # path('<int:event_id>/', views.RatingCreate.as_view(), name='rating_create'),
    path("<int:pk>/update", views.EventUpdate.as_view(), name="event_update"),
    path("<int:pk>/delete", views.EventDelete.as_view(), name="event_delete"),
    # path("rating/<int:pk>/", views.RatingDelete.as_view(), name="rating_delete"),
    path("nearby/", views.EventNearby.as_view(), name="event_nearby"),
]
