"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.shortcuts import redirect

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls', namespace='auth')),
    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('invoices/', include('invoices.urls', namespace='invoices')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('sales/', include('sales.urls', namespace='sales')),
    path('expenses/', include('expenses.urls', namespace='expenses')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('settings/', include('settings.urls', namespace='settings')),
]
