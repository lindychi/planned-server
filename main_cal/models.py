from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime

# Create your models here.
class Calendar(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    todo = models.OneToOneField('todo.Todo', on_delete=models.CASCADE)
    color = models.ForeignKey('config.Color', on_delete=models.CASCADE)

class Schedule(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    body = models.CharField(max_length=1024)
    todo = models.ForeignKey('todo.Todo', on_delete=models.CASCADE)
    calendar = models.ForeignKey('Calendar', on_delete=models.CASCADE)
    is_all_day = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=None)
    end_date = models.DateTimeField(default=None, null=True)
    category = models.CharField(max_length=64, default='time')

    def get_start_date(self):
        return get_datetime_str(self.start_date)

    def get_end_date(self):
        if self.end_date:
            return get_datetime_str(self.end_date)
        else:
            return get_datetime_str(timezone.now())
            # return get_datetime_str(self.start_date + datetime.timedelta(hours=1))

    def is_end(self):
        return (self.end_date != None)

def get_datetime_str(input):
    # return (input + datetime.timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
    return input.strftime('%Y-%m-%d %H:%M:%S%z')