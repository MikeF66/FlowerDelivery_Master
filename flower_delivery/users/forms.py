from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'phone', 'address')  # Указываем необходимые поля

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'phone', 'address')  # Указываем необходимые поля

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']  # Удаляем поле "Пароль", если оно добавляется автоматически