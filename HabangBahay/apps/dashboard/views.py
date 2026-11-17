# apps/dashboard/views.py
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
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

    if house.owner.id == user.id:
        messages.error(request, "You cannot rent your own house.")
        return redirect('dashboard:home')

    if request.method == 'POST':
        method = request.POST.get('payment_method')
        
        if not method:
            messages.error(request, "Please select a payment method.")
        else:
            sender, _ = Sender.objects.get_or_create(user=user)
            receiver, _ = Receiver.objects.get_or_create(user=house.Owner)
            
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

def inbox(request, active_user_id=None):
    if 'user_id' not in request.session:
        messages.error(request, 'Please login first.')
        return redirect('account:login')

    user = User.objects.get(id=request.session['user_id'])
    sender = user.get_or_create_sender()
    receiver = user.get_or_create_receiver()

    all_messages = Message.objects.filter(
        Q(sender=sender) | Q(receiver=receiver)
    ).select_related('sender__user', 'receiver__user').order_by('date_sent')

    conversations = {}
    for msg in all_messages:
        other_user = msg.receiver.user if msg.sender == sender else msg.sender.user
        
        if other_user.id not in conversations:
            conversations[other_user.id] = {
                'user': other_user,
                'last_message': msg,
                'messages': []
            }
        
        conversations[other_user.id]['messages'].append(msg)
        conversations[other_user.id]['last_message'] = msg

    active_conversation = None
    if active_user_id and int(active_user_id) in conversations:
        active_conversation = conversations[int(active_user_id)]

    context = {
        'user': user,
        'username': user.username,
        'conversations': conversations.values(),
        'active_conversation': active_conversation,
        'active_user_id': int(active_user_id) if active_user_id else None,
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
        
        active_user_id = request.POST.get('active_user_id') 

        if receiver_username:
            try:
                receiver_user = User.objects.get(username=receiver_username)
                if receiver_user.id == user.id:
                    messages.error(request, 'You cannot message yourself.')
                    return redirect('dashboard:inbox')
                
                active_user_id = receiver_user.id
            except User.DoesNotExist:
                messages.error(request, f'User "{receiver_username}" not found.')
                return redirect('dashboard:inbox')

        if not description:
            messages.error(request, 'Message cannot be empty.')
            return redirect('dashboard:inbox')
            
        if not active_user_id:
             messages.error(request, 'No recipient selected.')
             return redirect('dashboard:inbox')

        receiver_user = User.objects.get(id=active_user_id)
        sender = user.get_or_create_sender()
        receiver = receiver_user.get_or_create_receiver()

        Message.objects.create(
            sender=sender,
            receiver=receiver,
            description=description,
        )
        return redirect('dashboard:inbox_with_user', active_user_id=active_user_id)

    return redirect('dashboard:inbox')
