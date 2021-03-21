from django.shortcuts import render
from main_cal.models import Calendar
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    calendar = Calendar.objects.filter(user=User.objects.get(username='hanchi'))

    return render(request, 'main_cal/index.html', {'calendar':calendar})