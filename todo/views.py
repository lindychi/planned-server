import json
import datetime
from main_cal.models import Calendar, Schedule
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import IterTodo, Todo
from person.models import Person
from django.contrib.auth.models import User
from config.models import Config
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def todo_index(request):
    try:
        config = Config.objects.get(user=request.user)
    except Config.DoesNotExist:
        config = Config.objects.create(user=request.user)
        
    if not config.show_todo_complete:
        todos = Todo.objects.filter(parent=None, complete=False)
    else:
        todos = Todo.objects.filter(parent=None)

    my_schedules = Schedule.objects.filter(user=request.user)
    schedules = (my_schedules.filter(end_date__gte=timezone.now() - datetime.timedelta(days=7)) | my_schedules.filter(end_date=None))

    return render(request, 'todo/index.html', {'todos':todos, 'config':config, 'schedules':schedules})

def complete_todo(request):
    if request.method == 'POST':
        todo = Todo.objects.get(id=request.POST['tid'])
        todo.set_complete()

        context = {'complete':todo.get_complete()}
        return HttpResponse(json.dumps(context), content_type="application/json")

def complete_todo_get(request, tid):
    todo = Todo.objects.get(id=tid)
    todo.set_complete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

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

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def end_last_schedule(request, tid):
    todo = Todo.objects.get(id=tid)
    todo.end_last_schedule()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def todo_detail(request, tid):
    parent = Todo.objects.get(id=tid)
    todos = Todo.objects.filter(parent=parent)
    try:
        config = Config.objects.get(user=request.user)
    except Config.DoesNotExist:
        config = Config.objects.create(user=request.user)

    schedules = Schedule.objects.filter(user=request.user)

    return render(request, 'todo/index.html', {'parent':parent, 'todos':todos, 'config':config, 'schedules':schedules})

@login_required
def set_github_repo(request):
    if request.method == 'POST':
        tid = request.POST['tid']
        repo = request.POST['github_repo']

        todo = Todo.objects.get(id=tid, user=request.user)
        todo.github_repo = repo
        todo.save()
        
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

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

def ajax_todo_autocomplete(request):
    if request.is_ajax() and 'term' in request.GET:
        print(request.GET['term'])
        todos = Todo.objects.filter(name__icontains=request.GET['term'])[:10]
        results = []
        for p in todos:
            p_json = {}
            p_json['id'] = p.id
            p_json['label'] = p.name
            p_json['value'] = p.name
            results.append(p_json)
        data = json.dumps(results)
        mimetype = 'application/json'
        print(data)
        return HttpResponse(data, mimetype)
    return HttpResponse()

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

def disconnect_repo(request, tid):
    todo = Todo.objects.get(user=request.user, id=int(tid))
    todo.disconnect_repo()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def list(request):
    todo_list = (Todo.objects.filter(user=request.user, parent=None, last_update__lte=timezone.now()) | Todo.objects.filter(user=request.user, itertodo__isnull=False, due_date__lte=timezone.now())).order_by('complete', 'due_date', 'last_update')
    # todo_list = (Todo.objects.filter(user=request.user, parent=None) | Todo.objects.filter(user=request.user, itertodo__isnull=False)).order_by('complete', 'due_date', 'last_update')
    return render(request, 'todo/list.html', {'todo_list':todo_list})

@login_required
def add_itertodo(request):
    if request.method == "POST":
        parent = None
        name = ""
        delta = ""
        if 'parent' in request.POST and request.POST['parent']:
            parent = Todo.objects.get(id=request.POST['parent'])
        if 'name' in request.POST:
            name = request.POST['name']
        if 'delta' in request.POST:
            delta = request.POST['delta']

        # 이름이 입력되지 않았을경우엔 처리하지 않음
        if name:
            itertodo = IterTodo.objects.create(user=request.user, name=name, delta=delta)
            todo = Todo.objects.create(user=request.user, name=name, itertodo=itertodo, due_date=timezone.now())
            if parent:
                todo.set_parent(parent)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def update_todo_parent(request):
    if request.method == "POST":
        tid = request.POST['tid']
        parent = request.POST['parent']

        todo = Todo.objects.get(user=request.user, id=int(tid))
        parent = Todo.objects.get(user=request.user, name=parent)

        todo.set_parent(parent)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])