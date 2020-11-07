from django.db import models

# Create your models here.

class UserProfile(models.Model):
    """Customer's profile"""

    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female'),
        (2, 'not specified'),
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12)
    email = models.CharField(max_length=30)
    birth_date = models.DateField(max_length=8)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=2)
