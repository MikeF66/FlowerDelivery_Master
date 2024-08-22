from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Avg

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name = 'Название')
    short_description = models.CharField(max_length=250, verbose_name = 'Краткое описание')
    description = models.TextField(verbose_name = 'Полное описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name = 'Цена')
    image = models.ImageField(upload_to='products/', verbose_name = 'Изображение')
    available = models.BooleanField(default=True, verbose_name = 'В наличии')
    created = models.DateTimeField(auto_now=True,)
    updated = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return self.name

    def get_absolute_url(self): # Эта функция не используется
        return reverse('product_detail', args=[str(self.id)])

    def avg_rating(self):
        from reviews.models import Review
        reviews = Review.objects.filter(product=self)
        return reviews.aggregate(average=Avg('rating'))['average'] or 0


    def review_count(self):
        from reviews.models import Review
        count = Review.objects.filter(product=self).count()


        def get_pluralized_reviews(count):
            if count % 10 == 1 and count % 100 != 11:
                return 'отзыв'
            elif 2 <= count % 10 <= 4 and not (12 <= count % 100 <= 14):
                return 'отзыва'
            else:
                return 'отзывов'
        return (f' {count} {get_pluralized_reviews(count)}')






