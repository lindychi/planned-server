from django.urls import path, include
from . import views

app_name = 'person'

urlpatterns = [
    path('', views.person_index),
    path('update_commuincate/<int:pid>/', views.communicate_update_person, name='communicate_update_person'),
    path('update_meet/<int:pid>/', views.meet_update_person, name='meet_update_person'),
]
