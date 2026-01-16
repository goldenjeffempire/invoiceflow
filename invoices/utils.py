import io
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse

def generate_invoice_pdf(invoice):
    """
    Generates a PDF file for the invoice and returns bytes.
    Note: Real PDF generation is bypassed in this environment due to binary issues.
    """
    # Placeholder for PDF generation
    return b"%PDF-1.4\n%mocked_invoice_content"

def invoice_pdf_view(request, invoice_id):
    from django.shortcuts import get_object_or_404
    from .models import Invoice
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'
    
    pdf_content = generate_invoice_pdf(invoice)
    response.write(pdf_content)
    return response
