from django.urls import path, include
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.todo_index, name='index'),
    path('add_lower_todo/', views.add_lower_todo, name='add_lower_todo'),
    path('connect_top_to_calendar/<int:tid>/', views.connect_top_to_calendar, name='connect_top_to_calendar'),
    path('add_new_schedule/<int:tid>/', views.add_new_schedule, name='add_new_schedule'),
    path('end_last_schedule/<int:tid>/', views.end_last_schedule, name='end_last_schedule'),
    path('todo/detail/<int:tid>/', views.todo_detail, name="todo_detail"),
    path('todo/set_github_repo/', views.set_github_repo, name="set_github_repo"),
    path('todo/add_person/', views.add_person_to_todo, name="add_person_to_todo"),
    path('todo/remove_person/<int:tid>/<int:pid>', views.remove_person_from_todo, name="remove_person_from_todo"),
    path('todo/disconnect/repo/<int:tid>/', views.disconnect_repo, name="disconnect_repo"),
    path('list/', views.list, name="list"),
    path('add_itertodo/', views.add_itertodo, name="add_itertodo"),
    path('complete_todo_get/<int:tid>/', views.complete_todo_get, name='complete_todo_get'),

    path('ajax/complete/', views.complete_todo, name='complete_todo'),
    path('ajax/delete_todo/', views.delete_todo, name='delete_todo'),
    path('ajax/add_todo/', views.add_todo, name='add_todo'),
    path('ajax/person/autocomplete/', views.ajax_person_autocomplete, name='ajax_person_autocomplete')
]
