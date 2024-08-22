from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import messages

class EmailAuthenticationForm(AuthenticationForm):
    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        self.fields['username'].label = "Email"
        self.fields['username'].widget.attrs.update({'placeholder': 'Email'})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('catalog:home')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен')
            return redirect('users:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('catalog:home')
