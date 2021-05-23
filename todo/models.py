from django.conf import settings
from django.db import models
from config.models import Color
from main_cal.models import Calendar, Schedule
from django.urls import reverse

import random
import re
from django.utils import timezone

class IterTodo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024)
    delta = models.CharField(max_length=64)

# Create your models here.
class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('Todo', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=2048)
    complete = models.BooleanField(default=False)
    github_repo = models.CharField(max_length=256, blank=True, default="")
    persons = models.ManyToManyField('person.Person', default=None)
    itertodo = models.ForeignKey('IterTodo', on_delete=models.CASCADE, default=None, null=True)
    last_update = models.DateTimeField(default=None, null=True)

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

    def complete(self):
        self.complete = not self.complete
        if self.complete is True:
            self.update_last_update()

            for p in self.persons.all():
                p.update_meet()

        self.save()

    def update_last_update(self):
        self.last_update = timezone.now()
        self.save()
        if self.parent:
            self.parent.update_last_update()

    def get_last_update(self):
        if self.last_update:
            return self.last_update.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return ""
    
    def get_last_update_gap(self):
        if self.last_update:
            delta = timezone.now() - self.last_update
            seconds = delta.total_seconds()
            if seconds < 60:
                return "{}초 전".format(seconds)
            elif seconds < 3600:
                return "{}분 전".format(int(seconds / 60))
            elif seconds < 3600 * 24:
                return "{}시간 전".format(int(seconds / (3600 * 24)))
            elif delta.days < 7:
                return "{}일 전".format(delta.days)
            elif delta.days < 30:
                return "{}주 전".format(int(delta.days / 7))
            elif delta.days < 365:
                return "{}달 전".format(int(delta.days / 30))
            else:
                return "{}년 전".format(int(delta.days / 365))
        else:
            return ""
