from django.conf import settings
from django.db import models
from config.models import Color
from main_cal.models import Calendar, Schedule

import random

# Create your models here.
class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('Todo', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=2048)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return "[{0}] {1}".format(self.user, self.name)

    def get_child(self):
        return Todo.objects.filter(parent=self)

    def connect_to_calendar(self):
        color = random.choice(Color.objects.all())

        calendar = Calendar.objects.create(user=self.user, todo=self, color=color, title=self.name)
        calendar.save()
        
    def get_calendar(self):
        todo = self

        while todo.parent:
            todo = todo.parent

        return todo.calendar

    def last_schedule(self):
        schedule = Schedule.objects.filter(todo=self).last()
        return schedule