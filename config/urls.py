from django.urls import path, include
from . import views

app_name = 'config'

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/show_todo_complete/', views.ajax_show_todo_complete, name='ajax_show_todo_complete'),
]
