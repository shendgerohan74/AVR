# billing/views.py

from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import Invoice

def generate_invoice_pdf(request, invoice_id):
    invoice = Invoice.objects.get(invoice_id=invoice_id, patient=request.user)

    template = get_template('billing/invoice_pdf.html')
    html = template.render({"invoice": invoice})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice-{invoice.invoice_id}.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response
