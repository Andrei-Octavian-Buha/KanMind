"""
Authentication URL configuration.

Defines API endpoints for user registration, login, and logout.
"""
from django.urls import path
from .views import RegisterView, LogoutView, LoginView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('registration/', RegisterView.as_view(), name="registration"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout")
]