from django import forms
from .models import Car, Part

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            'name', 'year', 'price', 'color', 'mileage',
            'transmission', 'fuel_type', 'description', 'main_image'
        ]

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = [
            'name', 'price', 'rating', 'description', 'image'
        ]
