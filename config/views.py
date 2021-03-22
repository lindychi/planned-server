from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Config, Color

# Create your views here.
def index(request):
    config = Config.objects.get(user=User.objects.get(username='hanchi'))
    colors = Color.objects.all()
    return render(request, 'config/index.html', {'config':config, 'colors':colors})

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

def add_new_system_color(request):
    if request.method == 'POST':
        user = User.objects.get(username='hanchi')
        color = Color.objects.create(user=user, color=request.POST['color'], bg_color=request.POST['bg_color'],
                                    drag_bg_color=request.POST['bg_color'], border_color=request.POST['border_color'])
        color.save()
    return HttpResponseRedirect(reverse('config:index'))