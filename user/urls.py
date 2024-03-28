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
    path('rating/<int:pk>/', views.RatingCreate.as_view(), name='rating_create'),
    path("rating/<int:pk>/delete", views.RatingDelete.as_view(), name="rating_delete"),
    path('ratings/by-client/<int:pk>/', views.RatingIDClientListView.as_view(), name='ratings_by_client'),
    path("rating/<int:pk>/update", views.RatingUpdate.as_view(), name="rating_update"),
    path(
        "client/get/", views.ClientGetView.as_view(), name="client_data"
    ),
    path(
        "user/get/", views.UserGetView.as_view(), name="user_data"
    ),
]
