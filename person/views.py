from django.shortcuts import redirect, render
from .models import Person
from django.contrib.auth.decorators import login_required

def group_by_date(persons, column="last_communicate"):
    group_dict = {}
    for p in persons:
        if column == "last_communicate":
            if p.get_last_communicate_date() in group_dict:
                group_dict[p.get_last_communicate_date()].append(p)
            else:
                group_dict[p.get_last_communicate_date()] = [p]
        elif column == "last_meet":
            if p.get_last_meet_date() in group_dict:
                group_dict[p.get_last_meet_date()].append(p)
            else:
                group_dict[p.get_last_meet_date()] = [p]
    return group_dict

@login_required
def person_index(request):
    communicates = Person.objects.all().order_by('last_communicate', 'last_meet')
    communicates = group_by_date(communicates, column="last_communicate")
    meets = Person.objects.all().order_by('last_meet', 'last_communicate')
    meets = group_by_date(meets, column="last_meet")

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