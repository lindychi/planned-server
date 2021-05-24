from datetime import datetime, timedelta
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

    def __str__(self):
        return "{} {}마다".format(self.name, self.delta)

def rand_rgb():
    return random.randint(0, 255)

def color_gen():
    return "#{:02X}{:02X}{:02X}".format(rand_rgb(), rand_rgb(), rand_rgb())

# Create your models here.
class Todo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('Todo', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=2048)
    complete = models.BooleanField(default=False)
    github_repo = models.CharField(max_length=256, blank=True, default="")
    persons = models.ManyToManyField('person.Person', default=None, blank=True)
    itertodo = models.ForeignKey('IterTodo', on_delete=models.CASCADE, default=None, null=True)
    last_update = models.DateTimeField(default=None, null=True)
    due_date = models.DateTimeField(default=None, null=True)

    def __str__(self):
        if self.itertodo:
            return "{} {}까지".format(self.name, self.due_date)
        else:
            return "{0} {1}에 마지막으로".format(self.name, self.last_update)

    def get_child(self):
        return Todo.objects.filter(parent=self)

    def set_parent(self, parent):
        self.parent = parent
        self.save()

    def connect_to_calendar(self):
        try:
            color = random.choice(Color.objects.all())
        except Color.DoesNotExist:
            color = Color.objects.create(user=self.user, color=color_gen(), bg_color=color_gen(),
                                         drag_bg_color=color_gen(), border_color=color_gen())
        except IndexError:
            color = Color.objects.create(user=self.user, color=color_gen(), bg_color=color_gen(),
                                         drag_bg_color=color_gen(), border_color=color_gen())

        calendar = Calendar.objects.create(user=self.user, todo=self, color=color, title=self.name)
        calendar.save()
        
    def get_calendar(self):
        todo = self

        while todo.parent:
            todo = todo.parent

        try:
            calendar = todo.calendar
        except Calendar.DoesNotExist:
            self.connect_to_calendar()
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

    def get_complete(self):
        return self.complete

    def end_last_schedule(self):
        schedule = Schedule.objects.filter(todo=self).last()
        if schedule.end_date == None:
            schedule.set_end_date_now()

    def set_complete(self):
        self.complete = not self.get_complete()
        if self.get_complete() is True:
            self.update_last_update()
            self.end_last_schedule()

            for p in self.persons.all():
                p.update_meet()
        self.save()

        # 반복 할일일 경우의 처리
        if self.itertodo and Todo.objects.filter(user=self.user, itertodo=self.itertodo, due_date__gt=self.due_date).count() <= 0:
            # 좀 더 나중의 시간을 기준으로 다음 일정 추가
            if self.due_date >= timezone.now():
                date = self.due_date + timedelta(hours=9)
            else:
                date = timezone.now() + timedelta(hours=9)

            # timedelta 처리 추가
            if self.itertodo.delta[1:] == "일":
                date = date + timedelta(days=int(self.itertodo.delta[:1]))
                date = datetime(date.year, date.month, date.day) - timedelta(hours=9)
                Todo.objects.create(user=self.user, parent=self.parent, itertodo=self.itertodo, due_date=date, name=self.name)

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
    
    def time_gap(self, date):
        delta = timezone.now() - date
        seconds = delta.total_seconds()
        token = "전"
        if seconds < 0:
            token = "후"
        seconds = abs(seconds)
        if seconds <= 60:
            return "{}초 {}".format(int(seconds), token)
        elif seconds <= 3600:
            return "{}분 {}".format(int(seconds / 60), token)
        elif seconds <= 3600 * 24:
            return "{}시간 {}".format(int(seconds / (3600)), token)
        elif delta.days <= 7:
            return "{}일 {}".format(abs(delta.days), token)
        elif delta.days <= 30:
            return "{}주 {}".format(int(abs(delta.days) / 7), token)
        elif delta.days <= 365:
            return "{}달 {}".format(int(abs(delta.days) / 30), token)
        else:
            return "{}년 {}".format(int(abs(delta.days) / 365), token)

    def get_last_update_gap(self):
        if self.last_update:
            return self.time_gap(self.last_update)
        else:
            return ""

    def get_due_date_gap(self):
        if self.due_date:
            return self.time_gap(self.due_date)
        else:
            return ""

    def get_time_gap(self):
        if self.due_date:
            return self.get_due_date_gap()
        elif self.last_update:
            return self.get_last_update_gap()
        else:
            return ""
