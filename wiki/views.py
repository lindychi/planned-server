from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import Wiki
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
@login_required
def index(request):
    wikis = Wiki.objects.filter(user=request.user)
    return render(request, 'wiki/index.html', {'wikis':wikis})

@login_required
def add_wiki(request):
    if request.method == "POST":
        wiki = Wiki.objects.create(user=request.user, title=request.POST['title'], content="".join(request.POST['content']))
        return HttpResponseRedirect(reverse('wiki:index'))
    return render(request, 'wiki/add_wiki.html', {})

@login_required
def detail_wiki(request, wid):
    wiki = Wiki.objects.get(user=request.user, id=wid)
    return render(request, 'wiki/detail_wiki.html', {'wiki':wiki})