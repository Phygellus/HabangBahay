# apps/dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'  # <-- Add this

urlpatterns = [
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
]