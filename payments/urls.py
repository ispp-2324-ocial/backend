from django.urls import path
from . import views

urlpatterns = [
    path('home', views.HomePageView.as_view(), name='homepageview'),
    path('homepro', views.HomePageViewPro.as_view(), name='homepageviewpro'),
    path('config/', views.StripeConfig),
    path('create-checkout-session-basic/', views.CreateCheckoutSessionBasic),
    path('create-checkout-session-pro/', views.CreateCheckoutSessionPro),
    path('success/', views.SuccessView.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
]