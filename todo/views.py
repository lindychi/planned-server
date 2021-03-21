import json
from main_cal.models import Calendar, Schedule
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Todo
from django.contrib.auth.models import User
from config.models import Config
from django.utils import timezone

# Create your views here.
def todo_index(request):
    todos = Todo.objects.filter(parent=None)
    user=User.objects.get(username='hanchi')
    config = Config.objects.get(user=user)

    schedules = Schedule.objects.filter(user=user)

    return render(request, 'todo/index.html', {'todos':todos, 'config':config, 'schedules':schedules})

def complete_todo(request):
    if request.method == 'POST':
        todo = Todo.objects.get(id=request.POST['tid'])
        todo.complete = not todo.complete
        todo.save()

        context = {'complete':todo.complete}
        return HttpResponse(json.dumps(context), content_type="application/json")

def delete_todo(request):
    if request.method == 'POST':
        todo = Todo.objects.get(id=request.POST['tid'])
        todo.delete()

        context = {'tid':request.POST['tid']}
        return HttpResponse(json.dumps(context), content_type="application/json")

def add_todo(request):
    if request.method == 'POST':
        parent = Todo.objects.get(id=request.POST['tid'])
        user = User.objects.get(username='hanchi')
        # if todo.user == request.user:
        todo = Todo.objects.create(user=request.user, parent=parent, name=request.POST['name'])
        todo.save()

        context = {'name':todo.name}
        return HttpResponse(json.dumps(context), content_type="application/json")

def add_lower_todo(request):
    if request.method == 'POST':
        if 'tid' in request.POST:
            parent = Todo.objects.get(id=request.POST['tid'])
        else:
            parent = None
        user = User.objects.get(username='hanchi')
        # if todo.user == request.user:
        todo = Todo.objects.create(user=user, parent=parent, name=request.POST['name'])
        todo.save()

        return redirect('todo:index')

def connect_top_to_calendar(request, tid):
    # TODO: 본인 체크 필요
    todo = Todo.objects.get(id=tid)
    if not todo.parent:
        todo.connect_to_calendar()

    return redirect('todo:index')

def add_new_schedule(request, tid):
    todo = Todo.objects.get(id=tid)

    schedule = Schedule.objects.create(user=todo.user, title=todo.name, todo=todo, calendar=todo.get_calendar(), start_date=timezone.now())
    schedule.save()

    return redirect('todo:index')

def end_last_schedule(request, tid):
    todo = Todo.objects.get(id=tid)

    schedule = Schedule.objects.filter(todo=todo).last()
    schedule.end_date = timezone.now()
    schedule.save()

    return redirect('todo:index')

