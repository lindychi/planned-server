from django.shortcuts import redirect, render
from .models import Person
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def person_index(request):
    communicates = Person.objects.all().order_by('last_communicate', 'last_meet')
    meets = Person.objects.all().order_by('last_meet', 'last_communicate')

    return render(request, 'person/index.html', {'meets':meets, 'comus':communicates})

@login_required
def meet_update_person(request, pid):
    person = Person.objects.get(id=pid)
    person.update_meet()
    
    return redirect('/person')

@login_required
def communicate_update_person(request, pid):
    person = Person.objects.get(id=pid)
    person.update_communicate()

    return redirect('/person')

@login_required
def add_name(request):
    if request.method == 'POST':
        name = request.POST['name']
        person = Person.objects.create(user=request.user, name=name)
    return redirect('/person')