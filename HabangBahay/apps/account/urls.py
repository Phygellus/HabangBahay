# apps/account/urls.py
from django.urls import path
from . import views

app_name = 'account'  # <-- Add this

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    # Note: there is no logout here yet, so let's add it
]