from django.db import models

class House(models.Model):
    owner = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='houses')
    address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Any', 'Any')])
    rooms = models.IntegerField()
    availability = models.IntegerField(default=1)
    availability_status = models.CharField(max_length=20, choices=[('Available', 'Available'), ('Full', 'Full')], default='Available')

    def __str__(self):
        return f"{self.address} - {self.owner.username}"

class Message(models.Model):
    sender = models.ForeignKey('account.Sender', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('account.Receiver', on_delete=models.CASCADE, related_name='received_messages')
    description = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.user.username} to {self.receiver.user.username}"

class Payment(models.Model):
    sender = models.OneToOneField('account.Sender', on_delete=models.CASCADE)
    receiver = models.OneToOneField('account.Receiver', on_delete=models.CASCADE)
    house = models.ForeignKey('dashboard.House', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment #{self.id} - {self.house.address}"