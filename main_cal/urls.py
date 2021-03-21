from django.urls import path, include
from . import views

app_name = 'calendar'

urlpatterns = [
    path('', views.index),

    path('ajax_edit_schedule/', views.ajax_edit_schedule, name='ajax_edit_schedule'),
]
