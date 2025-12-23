from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
    # "title": "Projekt Y",
    title = models.CharField(max_length=100)
    # "owner_id": 3
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, blank=True, related_name='member_boards')
    
    def __str__(self):
        return self.title
    
    @property
    # "member_count": 12,
    def member_count(self):
        return self.members.count()

    @property
    # "ticket_count": 43,
    def ticket_count(self):
        return self.tasks.count()

    @property
    #"tasks_to_do_count": 12,
    def tasks_to_do_count(self):
        return self.tasks.filter(status='TODO').count()

    @property
    # "tasks_high_prio_count": 1,
    def tasks_high_prio_count(self):
        return self.tasks.filter(priority='HIGH').count()
