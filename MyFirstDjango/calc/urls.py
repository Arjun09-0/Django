from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calculate', views.calculate, name='calculate'), # Changed from 'add'
    path('dashboard/', views.dashboard, name='dashboard'),
]