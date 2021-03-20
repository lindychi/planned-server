import json
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Todo
from django.contrib.auth.models import User
from config.models import Config

# Create your views here.
def todo_index(request):
    todos = Todo.objects.filter(parent=None)
    config = Config.objects.get(user=User.objects.get(username='hanchi'))

    return render(request, 'todo/index.html', {'todos':todos, 'config':config})

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
