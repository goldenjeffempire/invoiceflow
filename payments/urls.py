from django.urls import path
from .views import payment_settings_view, invoice_payment_page, payment_success

app_name = 'payments'

urlpatterns += [
    path('settings/', payment_settings_view, name='payment_settings'),
    path('invoice/<int:invoice_id>/pay/', invoice_payment_page, name='invoice_payment'),
    path('success/<int:invoice_id>/<str:provider>/', payment_success, name='payment_success'),
    path('webhook/stripe/', stripe_webhook, name='stripe_webhook'),
    path('webhook/paystack/', paystack_webhook, name='paystack_webhook'),
]
