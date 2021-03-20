from django.db import models
from django.conf import settings

# Create your models here.

class Config(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    show_todo_complete = models.BooleanField(default=True)