from django.urls import path, include
from . import views

app_name = 'wiki'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_wiki/', views.add_wiki, name='add_wiki'),
    path('detail_wiki/<int:wid>/', views.detail_wiki, name='detail_wiki'),
]
