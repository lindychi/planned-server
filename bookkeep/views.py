from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Account, Installment
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
@login_required
def index(request):
    accounts = Account.objects.filter(user=request.user)
    installment = Installment.objects.filter(user=request.user)
    return render(request, 'bookkeep/index.html', {'accounts':accounts, 'installment':installment})

@login_required
def interest_free_installment(request):
    return render(request, 'bookkeep/interest_free_installment.html', {})

@login_required
def add_account(request):
    if request.method == "POST":
        account = Account.objects.create(user=request.user, title=request.POST['account'])
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def delete_account(request, aid):
    account = Account.objects.get(user=request.user, id=aid)
    account.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def add_installment(request):
    if request.method == "POST":
        print(request.POST)
        title = request.POST['title']
        account = Account.objects.get(user=request.user, title=request.POST['account'])
        interest_rate = float(request.POST['interest_rate'])
        repayment_method = request.POST['repayment_method']
        reimbursed_month = int(request.POST['reimbursed_month'])
        start_date = datetime.datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
        balance = int(request.POST['balance'])

        installment = Installment.objects.create(user=request.user, title=title, account=account, interest_rate=interest_rate,
                                                 repayment_method=repayment_method, reimbursed_month=reimbursed_month, 
                                                 start_date=start_date, balance=balance)
        installment.cal_paynode()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def recal_installment(request, iid):
    try:
        installment = Installment.objects.get(user=request.user, id=iid)
    except:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    paynodes = Paynode.objects.filter(user=request.user, installment=installment)
    paynodes.delete()

    installment.cal_paynode()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def delete_installment(request, iid):
    installment = Installment.objects.get(user=request.user, id=iid)
    installment.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

