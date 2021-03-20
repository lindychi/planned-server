from django.urls import path, include
from . import views

app_name = 'calendar'

urlpatterns = [
    path('', views.index),
]
