import json
from main_cal.models import Calendar, Schedule
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Todo
from person.models import Person
from django.contrib.auth.models import User
from config.models import Config
from django.utils import timezone
import json

# Create your views here.
def todo_index(request):
    todos = Todo.objects.filter(parent=None)
    try:
        config = Config.objects.get(user=request.user)
    except Config.DoesNotExist:
        config = Config.objects.create(user=request.user)

    schedules = Schedule.objects.filter(user=request.user)

    return render(request, 'todo/index.html', {'todos':todos, 'config':config, 'schedules':schedules})

def complete_todo(request):
    if request.method == 'POST':
        todo = Todo.objects.get(id=request.POST['tid'])
        todo.complete = not todo.complete
        todo.save()

        for p in todo.persons.all():
            p.update_meet()

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

        return HttpResponseRedirect(request.META['HTTP_REFERER'])

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

def todo_detail(request, tid):
    parent = Todo.objects.get(id=tid)
    todos = Todo.objects.filter(parent=parent)
    try:
        config = Config.objects.get(user=request.user)
    except Config.DoesNotExist:
        config = Config.objects.create(user=request.user)

    schedules = Schedule.objects.filter(user=request.user)

    return render(request, 'todo/index.html', {'parent':parent, 'todos':todos, 'config':config, 'schedules':schedules})

def add_person_to_todo(request):
    if request.method == "POST":
        person = Person.objects.get(user=request.user, name=request.POST['person'])
        todo = Todo.objects.get(user=request.user, id=request.POST['tid'])
        todo.add_person(person)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
def remove_person_from_todo(request, tid, pid):
    person = Person.objects.get(user=request.user, id=pid)
    todo = Todo.objects.get(user=request.user, id=tid)
    todo.remove_person(person)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def ajax_person_autocomplete(request):
    if request.is_ajax() and 'term' in request.GET:
        print(request.GET['term'])
        persons = Person.objects.filter(name__icontains=request.GET['term'])[:10]
        results = []
        for person in persons:
            person_json = {}
            person_json['id'] = person.id
            person_json['label'] = person.name
            person_json['value'] = person.name
            results.append(person_json)
        data = json.dumps(results)
        mimetype = 'application/json'
        print(data)
        return HttpResponse(data, mimetype)
    return HttpResponse()