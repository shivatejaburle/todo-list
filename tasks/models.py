from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    due_date = models.DateField(default=timezone.now, blank=True)
    task_owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def is_overdue(self):
        if self.due_date and datetime.now().date() > self.due_date:
            return True
        return False

    def __str__(self):
        return self.title