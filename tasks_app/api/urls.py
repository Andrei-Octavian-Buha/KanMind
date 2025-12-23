from django.urls import path
from .views import TasksAssignedToMeView, CreateNewTaskView

urlpatterns = [
    path('tasks/',CreateNewTaskView.as_view(),name='new-task'),
    path('tasks/assigned-to-me/', TasksAssignedToMeView.as_view(), name='assigned-to-me-list'),
]