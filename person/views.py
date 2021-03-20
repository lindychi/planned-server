from django.shortcuts import redirect, render
from .models import Person

# Create your views here.
def person_index(request):

    communicates = Person.objects.all().order_by('last_communicate', 'last_meet')
    meets = Person.objects.all().order_by('last_meet', 'last_communicate')

    return render(request, 'person/index.html', {'meets':meets, 'comus':communicates})

def meet_update_person(request, pid):
    person = Person.objects.get(id=pid)
    person.update_meet()
    
    return redirect('/person')

def communicate_update_person(request, pid):
    person = Person.objects.get(id=pid)
    person.update_communicate()

    return redirect('/person')