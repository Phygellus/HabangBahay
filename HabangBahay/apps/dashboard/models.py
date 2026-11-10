# apps/dashboard/models.py
from django.db import models

class House(models.Model):
    Owner = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='houses')
    Address = models.CharField(max_length=255)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Description = models.TextField()
    Gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Any', 'Any')])
    Rooms = models.IntegerField()
    Availability = models.IntegerField(default=1)
    Availability_Status = models.CharField(max_length=20, choices=[('Available', 'Available'), ('Full', 'Full')], default='Available')

    def __str__(self):
        return f"{self.Address} - {self.Owner.username}"

class Message(models.Model):
    sender = models.ForeignKey('account.Sender', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('account.Receiver', on_delete=models.CASCADE, related_name='received_messages')
    Description = models.TextField()
    Date_Sent = models.DateTimeField(auto_now_add=True)
    Is_Read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.user.username} to {self.receiver.user.username}"

class Payment(models.Model):
    sender = models.OneToOneField('account.Sender', on_delete=models.CASCADE)
    receiver = models.OneToOneField('account.Receiver', on_delete=models.CASCADE)
    Price = models.ForeignKey('dashboard.House', on_delete=models.CASCADE)
    Transaction_Date = models.DateTimeField(auto_now_add=True)
    Transaction_Method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment #{self.id}"