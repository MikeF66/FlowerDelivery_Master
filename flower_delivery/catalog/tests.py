from django.test import TestCase
from django.urls import reverse
from .models import Product

class ProductModelTestCase(TestCase):
    def setUp(self):
        # Создаем тестовый продукт
        self.product = Product.objects.create(
            name='Test Product',
            short_description='Short description of test product',
            description='Full description of test product',
            price=99.99,
            available=True
        )

    def test_product_creation(self):
        # Проверяем, что продукт создан корректно
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.short_description, 'Short description of test product')
        self.assertEqual(self.product.price, 99.99)
        self.assertTrue(self.product.available)

    def test_str_representation(self):
        # Проверяем корректность строкового представления продукта
        self.assertEqual(str(self.product), 'Test Product')

    def test_avg_rating(self):
        # Проверяем, что метод avg_rating возвращает 0, если отзывов нет
        self.assertEqual(self.product.avg_rating(), 0)

    def test_review_count(self):
        # Проверяем, что метод review_count возвращает корректное количество отзывов
        self.assertEqual(self.product.review_count(), ' 0 отзывов')
