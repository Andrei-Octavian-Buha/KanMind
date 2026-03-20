from django.db import models
from django.contrib.auth.models import User


class BoardsModel(models.Model):
    #"title": "neu"
    title = models.CharField(max_length=100)
    #"owner_id": 2
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #"members": []
    members = models.ManyToManyField(User, blank=True, related_name='member_boards')

    def __str__(self):
        return self.title
