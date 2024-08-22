from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser  # Используем кастомную модель пользователя
from orders.models import Order
from django.utils import timezone
from decimal import Decimal


class AdminPanelTests(TestCase):

    def setUp(self):
        # Создание пользователя с уникальным email для прав персонала
        self.staff_user = CustomUser.objects.create_user(username='staff', email='staff@example.com', password='password')
        self.staff_user.is_staff = True
        self.staff_user.save()

        # Создание клиента для имитации запросов
        self.client = Client()
        self.client.login(username='staff', password='password')

        # Создание тестового пользователя с уникальным email
        self.test_user = CustomUser.objects.create_user(username='testuser', email='testuser@example.com', password='password')

        # Создание тестового заказа с указанием customer
        self.order = Order.objects.create(
            order_date=timezone.now(),
            total_cost=Decimal('100.00'),
            status='new',
            customer=self.test_user  # Указание поля customer
        )

    def test_admin_orders_view(self):
        response = self.client.get(reverse('admin_panel:admin_orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel/admin_orders.html')
        self.assertIn('orders', response.context)

    def test_update_order_status(self):
        url = reverse('admin_panel:update_order_status', args=[self.order.id])

        # Выполняем POST-запрос, отправляя новый статус заказа
        response = self.client.post(url, {'status': 'completed'})
        self.assertEqual(response.status_code, 302)  # Проверка на редирект после обновления

    def test_delete_order(self):
        url = reverse('admin_panel:delete_order')
        response = self.client.get(url, {'order_id': self.order.id})
        self.assertEqual(response.status_code, 302)  # Проверка на редирект после удаления
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_admin_users_view(self):
        response = self.client.get(reverse('admin_panel:admin_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel/admin_users.html')
        self.assertIn('users', response.context)

    def test_user_detail_view(self):
        url = reverse('admin_panel:user_detail', args=[self.test_user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel/user_detail.html')
        self.assertIn('user', response.context)

    def test_delete_user(self):
        url = reverse('admin_panel:delete_user', args=[self.test_user.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Проверка на редирект после удаления
        self.assertFalse(CustomUser.objects.filter(id=self.test_user.id).exists())
