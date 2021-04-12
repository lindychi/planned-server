from django.db import models
from django.http import request
from django.conf import settings
from dateutil.relativedelta import relativedelta

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255)

class Installment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    interest_rate = models.FloatField()
    repayment_method = models.CharField(max_length=255)
    reimbursed_month = models.IntegerField()
    start_date = models.DateField()

    def cal_paynode(self):
        if self.repayment_method == "원리금균등상환":
            # 무이자
            if self.interest_rate <= 0:
                for index in range(self.reimbursed_month):
                    paynode = Paynode.objects.create(user=self.user, installment=self, account=self.account, 
                                                     title="{0} ({1}/{2})".format(self.title, index + 1, self.reimbursed_month),
                                                     balance=int(self.balance / self.reimbursed_month), 
                                                     paydate=(self.start_date + relativedelta(months=index)))
        else:
            return

    def get_paynodes(self):
        return Paynode.objects.filter(installment=self).order_by('paydate')
        

class Paynode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    installment = models.ForeignKey('Installment', on_delete=models.CASCADE, null=True, blank=True, default=None)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    balance = models.IntegerField()
    paydate = models.DateField()