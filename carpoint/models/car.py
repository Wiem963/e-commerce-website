from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=100)
    mileage = models.PositiveIntegerField()
    transmission = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=50)
    description = models.TextField()
    main_image = models.ImageField(upload_to='cars/main_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars', default=1)

    def __str__(self):
        return f"{self.name} ({self.year})"


class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cars/gallery_images/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.car.name}"
