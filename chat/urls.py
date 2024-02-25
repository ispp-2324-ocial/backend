from django.urls import path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('list/', views.ChatList.as_view(), name='chat_list'),
    path('<int:pk>/', views.ChatDetail.as_view(), name='chat_detail'),
    path('<int:chat_id>/create/', views.MessageCreate.as_view(), name='message_create'),
    path('<int:pk>/delete/', views.ChatDelete.as_view(), name='chat_delete'),
    path('message/<int:pk>/delete/', views.MessageDelete.as_view(), name='message_delete'),
    path('create/', views.ChatCreate.as_view(), name='chat_create'),
]
