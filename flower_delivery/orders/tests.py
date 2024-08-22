from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from .models import Order
from .forms import OrderForm
from django.template import Context, Template


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password")  # Использование кастомной модели пользователя
        self.order = Order.objects.create(
            customer=self.user,
            recipient_name='Test Recipient',
            recipient_phone='1234567890',
            delivery_address='Test Address',
            status='new',
            total_cost=100.00,
        )

    def test_order_creation(self):
        self.assertEqual(self.order.recipient_name, 'Test Recipient')
        self.assertEqual(self.order.total_cost, 100.00)

    def test_order_status_change(self):
        self.order.status = 'shipped'
        self.order.save()
        self.assertEqual(self.order.status, 'shipped')


class OrderFormTest(TestCase):

    def test_order_form_valid(self):
        form_data = {
            'recipient_name': 'Test Recipient',
            'recipient_phone': '1234567890',
            'delivery_address': 'Test Address',
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_form_invalid(self):
        form_data = {
            'recipient_name': '',
            'recipient_phone': 'invalid phone',
            'delivery_address': '',
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())


class OrderViewsTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", password="password")  # Использование кастомной модели пользователя
        self.client.login(username='testuser', password='password')

    def test_order_success_view(self):
        order = Order.objects.create(
            customer=self.user,
            recipient_name='Test Recipient',
            recipient_phone='1234567890',
            delivery_address='Test Address',
            status='new',
            total_cost=100.00,
        )
        response = self.client.get(reverse('orders:order_success', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_success.html')





