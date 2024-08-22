from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123',
            phone='1234567890',
            address='Test Address'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.phone, '1234567890')
        self.assertEqual(self.user.address, 'Test Address')
        self.assertTrue(self.user.check_password('testpassword123'))

    def test_str_method(self):
        self.assertEqual(str(self.user), self.user.email)


class CustomUserCreationFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'phone': '0987654321',
            'address': 'New Address',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'phone': '0987654321',
            'address': 'New Address',
            'password1': 'newpassword123',
            'password2': 'wrongpassword',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class CustomUserChangeFormTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )

    def test_valid_form(self):
        form_data = {
            'username': 'updateduser',
            'phone': '1112223333',
            'address': 'Updated Address',
        }
        form = CustomUserChangeForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())


class UserViewsTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )

    def test_register_view(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_profile_view(self):
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_logout_view(self):
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)  # Should redirect after logout


