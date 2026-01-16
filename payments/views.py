import stripe
from django.shortcuts import render, redirect, get_object_or_404
from invoices.models import Invoice
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import UserPaymentSettings, Payment
from .forms import PaymentSettingsForm
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import json

# Try to import paystackapi, but handle if it's mocked
try:
    from paystackapi.transaction import Transaction
except ImportError:
    Transaction = None

stripe.api_key = settings.STRIPE_SECRET_KEY

# type: ignore
@login_required
def payment_settings_view(request):
    settings_obj, created = UserPaymentSettings.objects.get_or_create(user=request.user) # type: ignore
    form = PaymentSettingsForm(request.POST or None, instance=settings_obj)
    
    if form.is_valid():
        form.save()
        messages.success(request, "Payment settings updated successfully.")
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
                    cancel_url=request.build_absolute_uri(f'/payments/cancel/{invoice.id}/stripe/'),
                    metadata={'invoice_id': str(invoice.id)}
                )
                return redirect(session.url)
            except Exception as e:
                messages.error(request, f"Stripe error: {e}")
        if provider == 'paystack':
            if Transaction: # type: ignore
                try:
                    paystack_settings = getattr(invoice.user, 'payment_settings', None)
                    if paystack_settings and paystack_settings.paystack_secret_key:
                        Transaction.secret_key = paystack_settings.paystack_secret_key # type: ignore
                        transaction = Transaction.initialize( # type: ignore
                            reference=f"INV-{invoice.id}-{invoice.user.id}",
                            amount=int(total_amount * 100),
                            email=invoice.client.email,
                            callback_url=request.build_absolute_uri(f'/payments/success/{invoice.id}/paystack/')
                        )
                        return redirect(transaction['data']['authorization_url'])
                    else:
                        messages.error(request, "Paystack is not configured for this user.")
                except Exception as e:
                    messages.error(request, f"Paystack error: {e}")
            else:
                messages.error(request, "Paystack is currently unavailable.")

    return render(request, 'invoices/invoice_payment.html', {'invoice': invoice, 'total_amount': total_amount})

@csrf_exempt
def payment_success(request, invoice_id, provider):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.status = 'paid'
    invoice.save()
    Payment.objects.create( # type: ignore
        invoice=invoice,
        user=invoice.user,
        amount=invoice.total_amount(),
        provider=provider,
        payment_id="verified_payment_id",
        status='succeeded'
    )
    messages.success(request, "Payment successful! Invoice marked as Paid.")
    return redirect('invoices:invoices_list')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        invoice_id = session['metadata'].get('invoice_id')
        invoice = Invoice.objects.filter(id=invoice_id).first() # type: ignore
        if invoice:
            if not Payment.objects.filter(payment_id=session['id']).exists(): # type: ignore
                Payment.objects.create( # type: ignore
                    invoice=invoice,
                    user=invoice.user,
                    amount=invoice.total_amount(),
                    provider='stripe',
                    payment_id=session['id'],
                    status='succeeded'
                )
                invoice.status = 'paid'
                invoice.save()
    return HttpResponse(status=200)

@csrf_exempt
def paystack_webhook(request):
    try:
        payload = json.loads(request.body)
        data = payload.get('data', {})
        reference = data.get('reference')
        status = data.get('status')
    except (json.JSONDecodeError, AttributeError):
        return HttpResponse(status=400)

    if Payment.objects.filter(payment_id=reference).exists(): # type: ignore
        return HttpResponse(status=200)

    try:
        parts = reference.split('-')
        invoice_id = int(parts[1])
        invoice = Invoice.objects.get(id=invoice_id) # type: ignore
    except Exception:
        return HttpResponse(status=400)

    if status == 'success':
        Payment.objects.create( # type: ignore
            invoice=invoice,
            user=invoice.user,
            amount=invoice.total_amount(),
            provider='paystack',
            payment_id=reference,
            status='succeeded'
        )
        invoice.status = 'paid'
        invoice.save()
    return HttpResponse(status=200)
