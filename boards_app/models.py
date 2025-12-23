from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
    # "title": "Projekt Y",
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, blank=True, related_name='member_boards')

    # "member_count": 12,
    # "ticket_count": 43,
    #     "tasks_to_do_count": 12,
    # "tasks_high_prio_count": 1,
    # "owner_id": 3
    def __str__(self):
        return self.title
    
    # Contorizări dinamice
    @property
    def member_count(self):
        return self.members.count()

    @property
    def ticket_count(self):
        return self.tasks.count()  # tasks = related_name din Task

    @property
    def tasks_to_do_count(self):
        return self.tasks.filter(status='TODO').count()

    @property
    def tasks_high_prio_count(self):
        return self.tasks.filter(priority='HIGH').count()
