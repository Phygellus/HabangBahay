from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    firstname = models.CharField(max_length=100, blank=True, default='')
    lastname = models.CharField(max_length=100, blank=True, default='')
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True, default='N/A')
    gender = models.CharField(
        max_length=10, 
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], 
        default='Other'
    )

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
    house = models.OneToOneField('dashboard.House', on_delete=models.CASCADE) 
    date_entered = models.DateField()
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')

    def __str__(self):
        return f"{self.user.username} - {self.house.address}"