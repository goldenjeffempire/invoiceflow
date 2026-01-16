import io
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from xhtml2pdf import pisa

def generate_invoice_pdf(invoice):
    """
    Generates a real PDF file for the invoice using xhtml2pdf.
    """
    html_content = render_to_string('invoices/invoice_pdf.html', {'invoice': invoice})
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(html_content.encode("UTF-8")), result)
    if not pisa_status.err:
        return result.getvalue()
    return None

def invoice_pdf_view(request, invoice_id):
    from django.shortcuts import get_object_or_404
    from .models import Invoice
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
    
    pdf_content = generate_invoice_pdf(invoice)
    if pdf_content:
        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'
        return response
    return HttpResponse(b"Error generating PDF", status=500) # type: ignore
