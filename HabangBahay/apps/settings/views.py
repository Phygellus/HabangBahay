from django.contrib import messages
from django.shortcuts import redirect, render
from apps.account.models import User

def home(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first.')
        return redirect('account:login')
    
    try:
        user = User.objects.get(id=request.session['user_id'])
    except User.DoesNotExist:
        request.session.flush()
        messages.error(request, 'User not found. Please login again.')
        return redirect('account:login')
    
    context = {
        'username': user.username,
        'email': user.email,
        'user_id': user.id,
    }
    return render(request, 'settings/settings.html', context)