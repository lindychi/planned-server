from django.urls import path, include
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.todo_index, name='index'),
    path('add_lower_todo/', views.add_lower_todo, name='add_lower_todo'),
    path('connect_top_to_calendar/<int:tid>/', views.connect_top_to_calendar, name='connect_top_to_calendar'),
    path('add_new_schedule/<int:tid>/', views.add_new_schedule, name='add_new_schedule'),
    path('end_last_schedule/<int:tid>/', views.end_last_schedule, name='end_last_schedule'),

    path('ajax/complete/', views.complete_todo, name='complete_todo'),
    path('ajax/delete_todo/', views.delete_todo, name='delete_todo'),
    path('ajax/add_todo/', views.add_todo, name='add_todo'),
]
