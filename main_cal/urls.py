from django.urls import path, include
from . import views

app_name = 'calendar'

urlpatterns = [
    path('', views.index),

    path('calendar/<int:cid>/change_random_color/', views.change_random_color, name='change_random_color'),

    path('ajax_edit_schedule/', views.ajax_edit_schedule, name='ajax_edit_schedule'),
]
