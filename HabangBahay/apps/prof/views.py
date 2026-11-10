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
    
    # Handle address update
    if request.method == 'POST':
        new_address = request.POST.get('address', '').strip()
        if not new_address:
            messages.error(request, 'Address cannot be empty.')
        else:
            user.Address = new_address
            user.save()
            messages.success(request, 'Address updated successfully!')
            return redirect('prof:home')
            
    context = {
        'username': user.username,
        'email': user.email,
        'address': user.Address,
    }
    return render(request, 'prof/profile.html', context)