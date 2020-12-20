from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):	
    """Customer's profile"""	

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Not_specified', 'Not_specified'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(max_length=30)
    telegram_id = models.CharField(null=True, blank=True, max_length=50)  # don`t show to user
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=13,choices=GENDER_CHOICES, default='Not_specified')

    def __str__(self):
        return f' {self.id} {self.user} {self.first_name}, {self.last_name} {self.phone_number} {self.telegram_id}'
