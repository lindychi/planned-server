from django.conf import settings
from django.db import models
from config.models import Color
from main_cal.models import Calendar, Schedule
from django.urls import reverse

import random
import re

# Create your models here.
class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('Todo', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=2048)
    complete = models.BooleanField(default=False)
    github_repo = models.CharField(max_length=256, blank=True, default="")
    persons = models.ManyToManyField('person.Person', default=None)

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

    def get_parents_link(self):
        html = ""
        ttodo = self.parent
        while ttodo is not None:
            html = "<a href='{}'>{}</a>".format(reverse('todo:todo_detail', args=[ttodo.id]), ttodo.name) + " > " + html
            ttodo = ttodo.parent
        html = "<a href='{}'>{}</a>".format(reverse('todo:index'), "main") + " > " + html

        return html

    def add_person(self, person):
        self.persons.add(person)
        self.save()

    def remove_person(self, person):
        self.persons.remove(person)
        self.save()

    def get_github_repo(self):
        repo = ""
        ttodo = self
        while ttodo is not None:
            if ttodo.github_repo:
                repo = ttodo.github_repo
                break
            ttodo = ttodo.parent
        return repo

    def get_name_with_link(self):
        name = self.name
        repo = self.get_github_repo()

        if '#' in name and repo:
            name = re.sub('#(\d+)', 
                          "<a href='https://github.com/{}/issues/\g<1>'>\g<0></a>".format(repo),
                          self.name)
        return name

    def disconnect_repo(self):
        self.github_repo = ""
        self.save()