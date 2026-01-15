import stripe
from django.shortcuts import render, redirect, get_object_or_404
from invoices.models import Invoice
from django.contrib.auth.decorators import login_required
from .models import UserPaymentSettings
from .forms import PaymentSettingsForm
from django.conf import settings
from django.contrib import messages
from .models import Payment
from paystackapi.transaction import Transaction
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def payment_settings_view(request):
    settings_obj, created = UserPaymentSettings.objects.get_or_create(user=request.user)
    form = PaymentSettingsForm(request.POST or None, instance=settings_obj)
    
    if form.is_valid():
        form.save()
        return redirect('payments:payment_settings')
    
    return render(request, 'settings/payment_settings.html', {'form': form})

def invoice_payment_page(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    total_amount = invoice.total_amount()

    if request.method == "POST":
        provider = request.POST.get('provider')
        if provider == 'stripe':
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {'name': f'Invoice #{invoice.id}'},
                            'unit_amount': int(total_amount * 100),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri(f'/payments/success/{invoice.id}/stripe/'),
                    cancel_url=request.build_absolute_uri(f'/payments/cancel/{invoice.id}/stripe/')
                )
                return redirect(session.url)
            except Exception as e:
                messages.error(request, f"Stripe error: {e}")
        elif provider == 'paystack':
            paystack_secret = invoice.user.payment_settings.paystack_secret_key
            Transaction.secret_key = paystack_secret
            transaction = Transaction.initialize(
                reference=f"INV-{invoice.id}-{invoice.user.id}",
                amount=int(total_amount * 100),
                email=invoice.client.email,
                callback_url=request.build_absolute_uri(f'/payments/success/{invoice.id}/paystack/')
            )
            return redirect(transaction['data']['authorization_url'])

    return render(request, 'invoices/invoice_payment.html', {'invoice': invoice, 'total_amount': total_amount})

@csrf_exempt
def payment_success(request, invoice_id, provider):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    # For simplicity, mark invoice as paid (webhooks will verify in Phase 7)
    invoice.status = 'paid'
    invoice.save()
    # Save Payment record
    Payment.objects.create(
        invoice=invoice,
        user=invoice.user,
        amount=invoice.total_amount(),
        provider=provider,
        payment_id="verified_payment_id",
        status='succeeded'
    )
    messages.success(request, "Payment successful! Invoice marked as Paid.")
    return redirect('invoices:invoices_list')
