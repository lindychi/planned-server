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
                                                     principal=int(self.balance / self.reimbursed_month),
                                                     balance=int(self.balance / self.reimbursed_month), 
                                                     paydate=(self.start_date + relativedelta(months=index)))
        elif self.repayment_method == "체증식상환":
            month_interest_rate = self.interest_rate / 12 / 100#월 이자 계산
            increase_principal = self.balance / (self.reimbursed_month - 1) / self.reimbursed_month * 2 #월 증액 상환 원금
            
            # 총 이자 계산
            iter_balance = self.balance # 감가할 원금
            total_interest = 0 # 총 이자금
            for index in range(self.reimbursed_month):
                total_interest = total_interest + iter_balance * month_interest_rate
                iter_balance = iter_balance - (index + 1) * increase_principal
            
            decrese_interest = total_interest / (self.reimbursed_month - 1) / self.reimbursed_month * 2

            interest_sum = 0
            principal_sum = 0
            for index in range(self.reimbursed_month):
                interest_value = (self.reimbursed_month - index - 1) * decrese_interest
                principal_value = index * increase_principal
                paynode = Paynode.objects.create(user=self.user, installment=self, account=self.account, 
                                                 title="{0} ({1}/{2})".format(self.title, index + 1, self.reimbursed_month),
                                                 principal=principal_value,
                                                 interest=interest_value,
                                                 balance=principal_value + interest_value, 
                                                 paydate=(self.start_date + relativedelta(months=index)))
                interest_sum = interest_sum + interest_value
                principal_sum = principal_sum + principal_value

            print("원금 {} == {}".format(self.balance, principal_sum))
            print("이자 {} == {}".format(total_interest, interest_sum))
        elif self.repayment_method == "대출고정상환":
            month_interest_rate = self.interest_rate / 12 / 100
            
            iter_balance = self.balance
            principal_value = int(self.balance / self.reimbursed_month)
            for index in range(self.reimbursed_month):
                interest_value = round(iter_balance * month_interest_rate, -2)
                paynode = Paynode.objects.create(user=self.user, installment=self, account=self.account, 
                                                 title="{0} ({1}/{2})".format(self.title, index + 1, self.reimbursed_month),
                                                 principal=principal_value,
                                                 interest=interest_value,
                                                 balance=principal_value + interest_value, 
                                                 paydate=(self.start_date + relativedelta(months=index)))
                print("{}월 잔액: {}".format(index + 1, iter_balance))
                iter_balance = iter_balance - principal_value
        else:
            return

    def get_paynodes(self):
        return Paynode.objects.filter(installment=self).order_by('paydate')
        

class Paynode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    installment = models.ForeignKey('Installment', on_delete=models.CASCADE, null=True, blank=True, default=None)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    interest = models.IntegerField(default=0)
    principal = models.IntegerField(default=0)
    balance = models.IntegerField()
    paydate = models.DateField()