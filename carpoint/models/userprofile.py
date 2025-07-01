from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES,default='customer' )
    phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='users/', default='users/default.png')
    address = models.CharField(max_length=150, default='Tunisia')
    def __str__(self):
        return f"{self.user.username} ({self.user_type})"
