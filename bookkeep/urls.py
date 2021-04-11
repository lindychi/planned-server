from django.urls import path, include
from . import views

app_name = 'bookkeep'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_account/', views.add_account, name="add_account"),
]
