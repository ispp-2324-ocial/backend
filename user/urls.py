from django.urls import path
from . import views

urlpatterns = [
    # URLs para usuarios
    path('user/register/', views.RegisterUserView.as_view(), name='user_register'),
    path('user/login/', views.LoginUserView.as_view(), name='user_login'),
    path('user/logout/', views.LogoutUserView.as_view(), name='user_logout'),
    
    # URLs para clientes
    path('client/register/', views.RegisterClientView.as_view(), name='client_register'),
    path('client/login/', views.LoginClientView.as_view(), name='client_login'),
    path('client/logout/', views.LogoutClientView.as_view(), name='client_logout'),
]

