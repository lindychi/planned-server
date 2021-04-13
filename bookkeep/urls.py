from django.urls import path, include
from . import views

app_name = 'bookkeep'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_account/', views.add_account, name="add_account"),
    path('delete_account/<int:aid>/', views.delete_account, name="delete_account"),
    path('add_installment/', views.add_installment, name="add_installment"),
    path('recal_installment/<int:iid>/', views.recal_installment, name="recal_installment"),
    path('delete_installment/<int:iid>/', views.delete_installment, name="delete_installment"),
    path('edit_installment/<int:iid>/', views.edit_installment, name="edit_installment"),
    path('simulation_view/', views.simulation_view, name="simulation_view"),
    path('congrestion_installment/', views.congrestion_installment, name="congrestion_installment"),
]
