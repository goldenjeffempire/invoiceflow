from django.urls import path
from .views import payment_settings_view

app_name = 'payments'

urlpatterns = [
    path('settings/', payment_settings_view, name='payment_settings'),
]
