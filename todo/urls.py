from django.urls import path, include
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.todo_index, name='index'),
    path('add_lower_todo/', views.add_lower_todo, name='add_lower_todo'),

    path('ajax/complete/', views.complete_todo, name='complete_todo'),
    path('ajax/delete_todo/', views.delete_todo, name='delete_todo'),
    path('ajax/add_todo/', views.add_todo, name='add_todo'),
]
