from django.urls import path
from . import views

urlpatterns = [
    # URLs para usuarios
    path('user/register/', views.RegisterUserView.as_view(), name='user_register'),
    path('login/', views.LoginUserView.as_view(), name='user_login'),
    path('logout/', views.LogoutUserView.as_view(), name='user_logout'),
    # URLs para clientes
    path('client/register/', views.RegisterClientView.as_view(), name='client_register'),
]