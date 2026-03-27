from datetime import date

from django.db import models
from django.contrib.auth.models import User
from boards_app.models import BoardsModel

# Create your models here.
class TaskModel(models.Model):
   
    STATUS_CHOICES = [
        ("to-do","to-do"),
        ("in-progress","in-progress"),
        ("review","review"),
        ("done","done"),
    ]

    class StatusPriority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high","High"
    board = models.ForeignKey(BoardsModel, on_delete=models.CASCADE)
    #"board": 12,
    #"title": "Code-Review durchführen",
    title = models.CharField(max_length=100)
    #"description": "Den neuen PR für das Feature X überprüfen",
    description = models.TextField(max_length=300)
    #   "status": "review",
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="to-do")
    #   "priority": "medium",
    priority = models.CharField(max_length=8, choices=StatusPriority.choices, default=StatusPriority.LOW)
    #   "assignee_id": 13,
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #   "reviewer_id": 1,
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    #   "due_date": "2025-02-27"
    due_date = models.DateField(default=date.today)
    # }