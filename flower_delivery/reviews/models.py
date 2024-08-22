from django.db import models
from users.models import CustomUser  # Импортируем вашу кастомную модель пользователя
from catalog.models import Product


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Используем вашу кастомную модель пользователя
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.product.name} - {self.rating}'



