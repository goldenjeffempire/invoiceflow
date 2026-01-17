from django.db import models
from django.conf import settings
from invoices.models import Invoice

# type: ignore
class UserPaymentSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_settings')
    
    # Stripe keys
    stripe_public_key = models.CharField(max_length=255, blank=True, null=True)
    stripe_secret_key = models.CharField(max_length=255, blank=True, null=True)
    
    # Paystack keys
    paystack_public_key = models.CharField(max_length=255, blank=True, null=True)
    paystack_secret_key = models.CharField(max_length=255, blank=True, null=True)
    paystack_webhook_url = models.URLField(blank=True, null=True)
    
    # Bank details
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    account_name = models.CharField(max_length=255, blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Payment Settings"

# type: ignore
class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments_list')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    provider = models.CharField(max_length=50)  # 'stripe' or 'paystack'
    payment_id = models.CharField(max_length=255)  # Stripe/Paystack transaction ID
    status = models.CharField(max_length=50, default='pending')  # pending, succeeded, failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} - {self.invoice_id} - {self.status}"
