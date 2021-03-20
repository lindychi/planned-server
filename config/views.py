from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Config

# Create your views here.
def index(request):
    config = Config.objects.get(user=User.objects.get(username='hanchi'))
    return render(request, 'config/index.html', {'config':config})

def ajax_show_todo_complete(request):
    show_todo_complete = False
    if 'show_todo_complete' in request.POST:
        if request.POST['show_todo_complete'] == 'true':
            show_todo_complete = True
            
    print("config set show_todo_complete: {} -> {}".format(request.POST['show_todo_complete'], show_todo_complete))
    user = User.objects.get(username='hanchi')
    
    try:
        config = Config.objects.get(user=user)
        config.show_todo_complete = show_todo_complete
        config.save()
    except Config.DoesNotExist:
        config = Config.objects.create(user=user, show_todo_complete=show_todo_complete)
        config.save()

    return HttpResponse('')
        