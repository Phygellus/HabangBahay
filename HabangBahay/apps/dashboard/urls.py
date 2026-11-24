# apps/dashboard/urls.py

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('payment/<int:house_id>/', views.payment, name='payment'),
    path('add-house/', views.add_house, name='add_house'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<int:active_user_id>/', views.inbox, name='inbox_with_user'), 
    path('send-message/', views.send_message, name='send_message'),
    path('owner-houses/', views.owner_houses, name='owner_houses'),
    path('renter-houses/', views.renter_houses, name='renter_houses'),
    path('transactions/', views.transaction_history, name='transaction_history'),
]