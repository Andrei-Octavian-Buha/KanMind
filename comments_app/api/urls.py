"""
URL configuration for comments API.

Defines endpoints for listing, creating, and deleting comments
associated with tasks.
"""
from django.urls import path
from .views import CommentListCreateView, CommentDeleteView

urlpatterns = [
    path("tasks/<int:task_id>/comments/", CommentListCreateView.as_view()),
    path("tasks/<int:task_id>/comments/<int:comment_id>/",CommentDeleteView.as_view()),
]