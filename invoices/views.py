from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client, Invoice, InvoiceItem
from .forms import ClientForm, InvoiceForm, InvoiceItemForm
from payments.utils import send_email
from .utils import generate_invoice_pdf
from django.utils.timezone import now, timedelta
from django import forms
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Sum

# type: ignore
@login_required
def clients_list(request):
    clients = Client.objects.filter(user=request.user)
    return render(request, 'invoices/clients.html', {'clients': clients})

@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            return redirect('invoices:clients_list')
    else:
        form = ClientForm()
    return render(request, 'invoices/client_form.html', {'form': form})

# -------- INVOICES --------
@login_required
def invoices_list(request):
    invoices = Invoice.objects.filter(user=request.user)
    return render(request, 'invoices/invoices.html', {'invoices': invoices})

@login_required
def invoice_create(request):
    ItemFormSet = forms.inlineformset_factory(Invoice, InvoiceItem, form=InvoiceItemForm, extra=1)
    
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        formset = ItemFormSet(request.POST)
        
        if invoice_form.is_valid() and formset.is_valid():
            invoice = invoice_form.save(commit=False)
            invoice.user = request.user
            invoice.save()
            formset.instance = invoice
            formset.save()
            return redirect('invoices:invoices_list')
    else:
        invoice_form = InvoiceForm()
        formset = ItemFormSet()
    
    return render(request, 'invoices/invoice_form.html', {'invoice_form': invoice_form, 'formset': formset})

def send_invoice_email(invoice):
    pdf_bytes = generate_invoice_pdf(invoice)
    payment_link = f"{settings.SITE_URL}/payments/invoice/{invoice.id}/pay/"
    html_content = render_to_string('emails/invoice_email.html', {
        'client_name': invoice.client.name,
        'invoice_id': invoice.id,
        'user_name': invoice.user.username,
        'total_amount': invoice.total_amount(),
        'due_date': invoice.due_date,
        'payment_link': payment_link
    })
    send_email(invoice.client.email, f"Invoice #{invoice.id}", html_content)

def send_payment_confirmation(invoice):
    html_content = render_to_string('emails/payment_confirmation.html', {
        'invoice_id': invoice.id,
        'total_amount': invoice.total_amount(),
    })
    send_email(invoice.client.email, f"Payment Received - Invoice #{invoice.id}", html_content)

def send_reminders():
    upcoming = Invoice.objects.filter(due_date__lte=now().date() + timedelta(days=3), auto_reminder=True, status='sent')
    for invoice in upcoming:
        payment_link = f"{settings.SITE_URL}/payments/invoice/{invoice.id}/pay/"
        html_content = render_to_string('emails/payment_reminder.html', {
            'invoice_id': invoice.id,
            'due_date': invoice.due_date,
            'payment_link': payment_link
        })
        send_email(invoice.client.email, f"Reminder: Invoice #{invoice.id} Due Soon", html_content)
