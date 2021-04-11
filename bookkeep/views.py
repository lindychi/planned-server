from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Account
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    if request.method == "POST":
        print(request.POST)
        title = request.POST['title']
        account = request.POST['account']
        interest_rate = float(request.POST['interest_rate'])
        repayment_method = request.POST['repayment_method']
        reimbursed_month = request.POST['reimbursed_month']
        start_date = request.POST['start_date']
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'bookkeep/index.html', {'accounts':accounts})

@login_required
def interest_free_installment(request):
    return render(request, 'bookkeep/interest_free_installment.html', {})

@login_required
def add_account(request):
    if request.method == "POST":
        account = Account.objects.create(user=request.user, title=request.POST['account'])
    return HttpResponseRedirect(request.META['HTTP_REFERER'])