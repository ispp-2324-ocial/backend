from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.ChatList.as_view(), name="chat_list"),
    path("<int:pk>/messages", views.ChatDetail.as_view(), name="chat_detail"),
    path(
        "<int:chat_id>/createMessage/",
        views.MessageCreate.as_view(),
        name="message_create",
    ),
    path("<int:pk>/delete/", views.ChatDelete.as_view(), name="chat_delete"),
    path(
        "<int:pk>/deleteMessage/", views.MessageDelete.as_view(), name="message_delete"
    ),
    path("create/", views.ChatCreate.as_view(), name="chat_create"),
]
