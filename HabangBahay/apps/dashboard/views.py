from django.contrib import messages
from django.shortcuts import redirect, render

# Create your views here.

def logout_view(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('account:login')
def home(request):
    # Check if user is logged in
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first.')
        return redirect('login')
    
    context = {
        'username': request.session.get('username', 'User')
    }
    
    return render(request, 'dashboard/home.html', context)  # ← Fixed path