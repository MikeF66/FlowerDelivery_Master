from django.test import TestCase
from django.conf import settings
from users.models import CustomUser
from .models import Review, Product
from .forms import ReviewForm


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password")  # Использование кастомной модели пользователя
        self.product = Product.objects.create(name="Test Product", price=100.00)  # Указание цены продукта
        self.review = Review.objects.create(
            comment="Test content",
            rating=5,
            product=self.product,  # Указание продукта для отзыва
            user=self.user  # Указание пользователя для отзыва
        )

    def test_review_creation(self):
        self.assertEqual(self.review.comment, "Test content")
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.user, self.user)  # Проверка связи с пользователем

class ReviewFormTest(TestCase):
    def test_valid_form(self):
        form_data = {'comment': "Test content", 'rating': 5}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'comment': "Test content", 'rating': 0}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())




