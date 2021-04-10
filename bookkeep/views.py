from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    if request.method == "POST":
        print(request.POST)
        title = request.POST['title']
        account = request.POST['account']
        interest_rate = float(request.POST['interest_rate'])
        repayment_method = request.POST['repayment_method']
        reimbursed_month = request.POST['reimbursed_month']
        start_date = request.POST['start_date']
    return render(request, 'bookkeep/index.html', {})

def interest_free_installment(request):
    return render(request, 'bookkeep/interest_free_installment.html', {})