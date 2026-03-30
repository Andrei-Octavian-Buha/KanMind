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
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="to-do")
    priority = models.CharField(max_length=8, choices=StatusPriority.choices, default=StatusPriority.LOW)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_tasks")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="review_tasks")
    due_date = models.DateField(default=date.today)

    def __str__(self):
        return self.title