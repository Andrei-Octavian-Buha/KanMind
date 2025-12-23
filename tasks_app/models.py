from django.db import models
from django.db.models.functions import Now
from django.contrib.auth.models import User
from boards_app.models import Board


# Create your models here.

class Task(models.Model):
    STATUS_CHOICES = [
        ("TODO","to-do"),
        ("INPROGRESS","in-progress"),
        ("REVIEW","review"),
        ("DONE","done")
    ]
    PRIORITY_CHOICES = [
        ("LOW","low"),
        ("MEDIUM","medium"),
        ("HIGH","high")
    ]
        #   "board": 12,
    board = models.ForeignKey(Board,on_delete=models.CASCADE,related_name='tasks')
    #   "title": "Code-Review durchführen",
    title = models.CharField(max_length=100)
    #   "description": "Den neuen PR für das Feature X überprüfen",
    description = models.TextField(blank=True) 
    #   "status": "review",
    status = models.CharField(max_length=11,choices=STATUS_CHOICES, default="TODO")   
    #   "priority": "medium",
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default="MEDIUM", blank=True)
    #   "assignee_id": 13,
    assigned = models.ManyToManyField(User,blank=True, related_name='assigned_tasks')
    #   "reviewer_id": 1,
    reviewer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='reviewer_tasks')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tasks')
    due_date = models.DateTimeField(db_default=Now())
