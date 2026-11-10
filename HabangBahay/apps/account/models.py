# apps/account/models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    Address = models.CharField(max_length=255, blank=True, default='N/A')

    def __str__(self):
        return self.username
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Sender(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sender: {self.user.username}"

class Receiver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Receiver: {self.user.username}"

class House_Renter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # We use a string reference so Django doesn't crash if House isn't defined yet
    house = models.OneToOneField('dashboard.House', on_delete=models.CASCADE) 
    Date_Entered = models.DateField()
    Status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')