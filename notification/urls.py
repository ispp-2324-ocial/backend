from django.urls import path

from . import views

urlpatterns = [
    path("view/", views.index,),
    path("create/", views.NotificationCreate.as_view(), name="notification"),
    path("<int:pk>/update/", views.NotificationUpdate.as_view(), name="notification_update"),
    path("<int:pk>/delete/", views.NotificationDelete.as_view(), name="notification_delete"),
]
