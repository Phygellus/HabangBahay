# apps/dashboard/views.py
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from apps.account.models import User, Sender, Receiver
from .models import House, Payment

def logout_view(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('account:login')

def home(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first.')
        return redirect('account:login')
    
    user = User.objects.get(id=request.session['user_id'])
    
    # FIX: Use lowercase availability_status
    houses = House.objects.filter(availability_status='Available')
    
    context = {
        'username': user.username,
        'houses': houses,
    }
    return render(request, 'dashboard/home.html', context)

def payment(request, house_id):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first.')
        return redirect('account:login')
    
    user = User.objects.get(id=request.session['user_id'])
    house = get_object_or_404(House, id=house_id)

    # Prevent owners from paying themselves
    if house.Owner.id == user.id:
        messages.error(request, "You cannot rent your own house.")
        return redirect('dashboard:home')

    if request.method == 'POST':
        method = request.POST.get('payment_method')
        
        if not method:
            messages.error(request, "Please select a payment method.")
        else:
            # Auto-create Sender/Receiver if they don't exist
            sender, _ = Sender.objects.get_or_create(user=user)
            receiver, _ = Receiver.objects.get_or_create(user=house.Owner)
            
            # Create payment record
            Payment.objects.create(
                sender=sender,
                receiver=receiver,
                Price=house,
                Transaction_Method=method
            )
            
            messages.success(request, f"Successfully paid for {house.Address}!")
            return redirect('dashboard:home')

    context = {
        'username': user.username,
        'house': house,
    }
    return render(request, 'dashboard/payment.html', context)