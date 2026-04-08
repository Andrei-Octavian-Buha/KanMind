"""
URL configuration for boards API.

Registers the BoardsViewSet using a SimpleRouter,
exposing RESTful endpoints for board management.
"""
from django.urls import path 
from rest_framework import routers 
from .views import BoardsViewSet


router = routers.SimpleRouter()
router.register(r'boards', BoardsViewSet, basename='board')

urlpatterns = router.urls