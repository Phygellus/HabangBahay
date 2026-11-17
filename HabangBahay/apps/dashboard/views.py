# apps/dashboard/views.py
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from apps.account.models import User, Sender, Receiver
from .models import House, Payment, Message


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
    if house.owner.id == user.id:
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

def add_house(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first.')
        return redirect('account:login')
    
    user = User.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        address = request.POST.get('address')
        price = request.POST.get('price')
        description = request.POST.get('description')
        gender = request.POST.get('gender')
        rooms = request.POST.get('rooms')

        if not address or not price or not description or not rooms:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'dashboard/add_house.html')

        # Create the house
        House.objects.create(
            owner=user,
            address=address,
            price=price,
            description=description,
            gender=gender,
            rooms=rooms,
            availability_status='Available'
        )

        messages.success(request, 'House added successfully!')
        return redirect('dashboard:home')

    return render(request, 'dashboard/add_house.html')

def inbox(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first.')
        return redirect('account:login')

    user = User.objects.get(id=request.session['user_id'])

    sender = user.get_or_create_sender()
    receiver = user.get_or_create_receiver()

    received_messages = Message.objects.filter(
        receiver=receiver
    ).select_related('sender__user').order_by('-date_sent')

    sent_messages = Message.objects.filter(
        sender=sender
    ).select_related('receiver__user').order_by('-date_sent')

    context = {
        'user': user,
        'username': user.username,
        'email': user.email,
        'sender': sender,
        'receiver': receiver,
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    }
    return render(request, 'dashboard/inbox.html', context)

def send_message(request):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first.')
        return redirect('account:login')

    user = User.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        receiver_username = request.POST.get('receiver_username')
        description = request.POST.get('description')

        if not receiver_username or not description:
            messages.error(request, 'All fields are required.')
            return redirect('dashboard:inbox')

        try:
            receiver_user = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            messages.error(request, f'User "{receiver_username}" not found.')
            return redirect('dashboard:inbox')

        if receiver_user.id == user.id:
            messages.error(request, 'You cannot send a message to yourself.')
            return redirect('dashboard:inbox')

        sender = user.get_or_create_sender()
        receiver = receiver_user.get_or_create_receiver()

        Message.objects.create(
            sender=sender,
            receiver=receiver,
            description=description,
        )

        messages.success(request, f'Message sent to {receiver_user.username}!')
        return redirect('dashboard:inbox')

    return redirect('dashboard:inbox')