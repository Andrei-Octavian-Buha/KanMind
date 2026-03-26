from rest_framework import routers
from .views import TasksViewSet

router = routers.SimpleRouter()
router.register(r'tasks', TasksViewSet)

urlpatterns = router.urls