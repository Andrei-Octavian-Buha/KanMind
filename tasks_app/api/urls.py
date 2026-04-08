from rest_framework import routers
from .views import TasksViewSet
"""
Router configuration for Tasks API.

Uses SimpleRouter from Django REST Framework to automatically generate
CRUD routes and custom @action endpoints defined in TasksViewSet.
"""
router = routers.SimpleRouter()
# Registers TasksViewSet under root path of this app.
# Example endpoints generated:
# - GET /               -> retrieve/list (depending on mixins used)
# - POST /              -> create task
# - GET /{id}/          -> retrieve task
# - PUT/PATCH /{id}/    -> update task
# - DELETE /{id}/       -> delete task
# - GET /assigned-to-me/
# - GET /reviewing/
router.register(r'', TasksViewSet)

urlpatterns = router.urls