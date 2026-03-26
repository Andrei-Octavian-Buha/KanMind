from django.urls import path 
from rest_framework import routers 
from .views import BoardsViewSet


router = routers.SimpleRouter()
router.register(r'boards', BoardsViewSet)

urlpatterns = router.urls