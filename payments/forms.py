from django import forms
from .models import UserPaymentSettings

class PaymentSettingsForm(forms.ModelForm):
    class Meta:
        model = UserPaymentSettings
        fields = [
            'stripe_public_key', 'stripe_secret_key',
            'paystack_public_key', 'paystack_secret_key', 'paystack_webhook_url',
            'bank_name', 'account_number', 'account_name'
        ]
        widgets = {
            'stripe_secret_key': forms.PasswordInput(render_value=True),
            'paystack_secret_key': forms.PasswordInput(render_value=True),
        }
