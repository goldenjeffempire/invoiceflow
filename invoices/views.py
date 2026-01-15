from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client, Invoice, InvoiceItem
from .forms import ClientForm, InvoiceForm, InvoiceItemForm

# -------- CLIENTS --------
@login_required
def clients_list(request):
    clients = Client.objects.filter(user=request.user)
    return render(request, 'invoices/clients.html', {'clients': clients})

@login_required
def client_create(request):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        client = form.save(commit=False)
        client.user = request.user
        client.save()
        return redirect('invoices:clients_list')
    return render(request, 'invoices/client_form.html', {'form': form})

# -------- INVOICES --------
@login_required
def invoices_list(request):
    invoices = Invoice.objects.filter(user=request.user)
    return render(request, 'invoices/invoices.html', {'invoices': invoices})

@login_required
def invoice_create(request):
    invoice_form = InvoiceForm(request.POST or None)
    ItemFormSet = forms.inlineformset_factory(Invoice, InvoiceItem, form=InvoiceItemForm, extra=1)
    formset = ItemFormSet(request.POST or None)
    
    if invoice_form.is_valid() and formset.is_valid():
        invoice = invoice_form.save(commit=False)
        invoice.user = request.user
        invoice.save()
        formset.instance = invoice
        formset.save()
        return redirect('invoices:invoices_list')
    
    return render(request, 'invoices/invoice_form.html', {'invoice_form': invoice_form, 'formset': formset})
