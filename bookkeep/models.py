from django.db import models
from django.http import request
from django.conf import settings

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255)

class Installment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    interest_rate = models.FloatField()
    repayment_method = models.CharField(max_length=255)
    reimbursed_month = models.IntegerField()
    start_date = models.DateField()