from django.db import models

# Create your models here.

class UserProfile(models.Model):
    """Customer's profile"""
    
    Male = 'Male'
    Female = 'Female'
    Not_specified = 'not specified'

    GENDER_CHOICES = (
        (Male, 'Male'),
        (Female, 'Female'),
        (Not_specified, 'not specified'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(max_length=30)
    birth_date = models.DateField(null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=Not_specified,)
