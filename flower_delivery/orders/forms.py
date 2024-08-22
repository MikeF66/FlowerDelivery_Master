from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['recipient_name', 'recipient_phone', 'delivery_address']
        labels = {
            'recipient_name': 'Получатель',
            'recipient_phone': 'Телефон получателя',
            'delivery_address': 'Адрес доставки',
        }