# apps/account/views.py

from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
            return render(request, 'account/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'account/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'account/register.html')
        
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )
        user.save()
        
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('account:login')  # <-- FIXED
    
    return render(request, 'account/register.html')

def login_view(request):
    if 'user_id' in request.session:
        return redirect('dashboard:home')  # <-- FIXED (points to dashboard app)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return render(request, 'account/login.html')
        
        try:
            user = User.objects.get(email=email)
            
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard:home')  # <-- FIXED
            else:
                messages.error(request, 'Invalid password.')
                return render(request, 'account/login.html')
                
        except User.DoesNotExist:
            messages.error(request, 'Email not registered. Please register first.')
            return render(request, 'account/login.html')
    
    return render(request, 'account/login.html')