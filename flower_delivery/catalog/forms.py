from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'short_description', 'description', 'price', 'image', 'available']
        labels = {
            'name': 'Название',
            'short_description': 'Краткое описание',
            'description': 'Полное описание',
            'price': 'Цена',
            'image': 'Изображение',
            'available': 'В наличии'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
