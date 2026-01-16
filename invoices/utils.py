import io
from django.template.loader import render_to_string
from xhtml2pdf import pisa

def generate_invoice_pdf(invoice):
    """
    Generates a PDF file for the invoice and returns bytes
    """
    html = render_to_string('invoices/invoice_pdf.html', {'invoice': invoice})
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None
