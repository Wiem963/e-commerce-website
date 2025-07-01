from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Deal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deals_made')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deals_received')
    proposal = models.DecimalField(max_digits=10, decimal_places=2)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(auto_now_add=True)

    def get_product_detail_url(self):
        product = self.product
        if not product:
            return '#'

        model_name = product._meta.model_name

        if model_name == 'car':
            return reverse('car_details', args=[product.id])
        elif model_name == 'part':
            return reverse('part_details', args=[product.id])
        else:
            return '#'

    def get_product_image_url(self):
        product = self.product
        if not product:
            return ''

        if hasattr(product, 'main_image'):
            return product.main_image.url if product.main_image else ''
        elif hasattr(product, 'image'):
            return product.image.url if product.image else ''
        else:
            return ''

    def __str__(self):
        return f"Deal from {self.customer.username} to {self.seller.username} for {self.product}"
