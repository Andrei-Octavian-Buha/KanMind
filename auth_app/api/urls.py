from django.urls import path
from .views import RegisterView, LogoutView, UserPorfileList, LoginView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('profiles/', UserPorfileList.as_view(), name = 'userprofile-list'),
    path('registration/', RegisterView.as_view(), name="registration"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout")
]