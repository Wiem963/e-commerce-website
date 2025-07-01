from django.db import models
from django.contrib.auth.models import User

class Part(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='parts/main_images/')
    description = models.TextField(blank=True)
    rating = models.FloatField(default=0)
    reviews_count = models.PositiveIntegerField(default=0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parts', default=2)

    def __str__(self):
        return self.name



class PartImage(models.Model):
    part = models.ForeignKey(Part, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='parts/gallery_images/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.part.name}"
