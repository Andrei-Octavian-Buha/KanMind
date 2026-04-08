from django.db import models
from django.contrib.auth.models import User 
from tasks_app.models import TaskModel

class Comment(models.Model):
    """
    Represents a comment on a task.

    Each comment is linked to:
    - a task (parent entity)
    - an author (user who created it)

    Used for collaboration and discussion within tasks.
    """
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a short textual representation of the comment.

        Returns:
            str: Comment content (truncated implicitly in admin if needed)
        """
        return self.content