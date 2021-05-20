from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Person(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    resi_number = models.CharField(max_length=24, blank=True, default='')
    last_meet = models.DateField(null=True, blank=True, default=None)
    last_communicate = models.DateField(null=True, blank=True, default=None)

    def __str__(self):
        return "[{0}] {1}".format(self.user, self.name)

    def update_meet(self):
        self.last_meet = timezone.now()
        self.last_communicate = timezone.now()
        self.save()

    def update_communicate(self):
        self.last_communicate = timezone.now()
        self.save()

    def get_last_meet_date(self):
        return self.last_meet.strftime('%Y-%m-%d')
    
    def get_last_communicate_date(self):
        return self.last_communicate.strftime('%Y-%m-%d')

class PersonComment(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    comment = models.CharField(max_length=2048)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)