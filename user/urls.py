from django.urls import path
from . import views

urlpatterns = [
    # URLs para usuarios
    path("user/register/", views.RegisterUserView.as_view(), name="user_register"),
    path("login/", views.LoginUserView.as_view(), name="user_login"),
    path("logout/", views.LogoutUserView.as_view(), name="user_logout"),
    # URLs para clientes
    path(
        "client/register/", views.RegisterClientView.as_view(), name="client_register"
    ),
    path(
        "user/google-oauth2/", views.GoogleSocialAuthView.as_view(), name="google_auth"
    ),
    path('rating/', views.RatingCreate.as_view(), name='rating_create'),
    path("rating/<int:pk>/", views.RatingDelete.as_view(), name="rating_delete"),
    path('ocialclients', views.ClientIDListView.as_view(), name='get_ocialclients'),
]
