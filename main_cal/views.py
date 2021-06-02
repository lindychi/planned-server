from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from main_cal.models import Calendar, Schedule
from django.contrib.auth.models import User
from django.urls import reverse

import datetime
from dateutil.parser import parse

# Create your views here.
def index(request):
    calendar = Calendar.objects.filter(user=User.objects.get(username='hanchi'))

    return render(request, 'main_cal/index.html', {'calendar':calendar})

def jdatetime_to_pdatetime(jdatetime_str):
    end_date = (jdatetime_str.split('(')[0]).strip(' ')
    return datetime.datetime.strptime(end_date, '%a %b %d %Y %H:%M:%S %Z%z')

def ajax_edit_schedule(request):
    if request.method == 'POST':
        if 'schedule_id' in request.POST:
            schedule = Schedule.objects.get(id=request.POST['schedule_id'])

            if 'end_date' in request.POST:
                schedule.end_date = jdatetime_to_pdatetime(request.POST['end_date'])

            if 'start_date' in request.POST:
                schedule.start_date = jdatetime_to_pdatetime(request.POST['start_date'])
                
            schedule.save()

    return HttpResponse()

def change_random_color(request, cid):
    calendar = Calendar.objects.get(id=cid)
    calendar.change_random_color()
    return HttpResponseRedirect(reverse('todo:index'))

def ajax_delete_schedule(request):
    if request.method == 'POST':
        if 'schedule_id' in request.POST:
            schedule = Schedule.objects.get(id=request.POST['schedule_id'])
            schedule.delete()
    return HttpResponse()
