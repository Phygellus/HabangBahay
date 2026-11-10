# apps/dashboard/urls.py

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('payment/<int:house_id>/', views.payment, name='payment'),
    path('add-house/', views.add_house, name='add_house'), # <-- Add this line
]