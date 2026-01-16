from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, LoginForm
from django.core.exceptions import PermissionDenied
from .decorators import admin_required

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard:home')
    return render(request, 'auth/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('dashboard:home')
    return render(request, 'auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('auth:login')

@admin_required
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')
