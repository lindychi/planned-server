from django.db import models
from django.conf import settings

# Create your models here.

class Config(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    show_todo_complete = models.BooleanField(default=True)

class Color(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    color = models.CharField(max_length=12, default='#ffffff')
    bg_color = models.CharField(max_length=12, default='#000000')
    drag_bg_color = models.CharField(max_length=12, default='#000000')
    border_color = models.CharField(max_length=12, default='#ffffff')
