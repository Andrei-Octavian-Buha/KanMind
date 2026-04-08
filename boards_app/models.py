from django.db import models
from django.contrib.auth.models import User


class BoardsModel(models.Model):
    """
    Represents a Kanban board.

    A board is owned by a single user and can have multiple members.
    Used as the main container for tasks and project organization.
    """
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, blank=True, related_name='member_boards')

    def __str__(self):
        """
        String representation of the board.

        Returns:
            str: Board title
        """
        return self.title
