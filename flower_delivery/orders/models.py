from django.db import models
from django.conf import settings
from catalog.models import Product
import jsonfield

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Заказчик')
    recipient_name = models.CharField(max_length=100, verbose_name='Получатель')
    products = jsonfield.JSONField(verbose_name='Товары')
    recipient_phone = models.CharField(max_length=25, verbose_name='Телефон получателя')
    delivery_address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def str(self):
        return f'Order {self.id} by {self.customer}'



    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')

    def str(self):
        return f'Cart for {self.user.username}'

    def get_total_cost(self):
        return sum(item.get_total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def str(self):
        return f'{self.quantity} x {self.product.name}'

    def get_total_price(self):
        return self.quantity * self.product.price



