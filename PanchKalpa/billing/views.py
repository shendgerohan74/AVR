import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Invoice


# -----------------------------
# BILLING HOME PAGE
# -----------------------------

@login_required
def billing_home(request):
    print("✅ USING BILLING HOME VIEW")

    pending = Invoice.objects.filter(patient=request.user, status="issued")
    history = Invoice.objects.filter(patient=request.user, status="paid")

    print("\n================ DEBUG BILLING ================")
    print("LOGGED USER:", request.user, request.user.email)
    print("PENDING:", list(pending))
    print("HISTORY:", list(history))
    print("===============================================\n")

    return render(request, "patient-portal/billing.html", {
        "pending": pending,
        "history": history
    })

# -----------------------------
# CREATE RAZORPAY ORDER
# -----------------------------
@login_required
def create_order(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, patient=request.user)

    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    order_data = {
        "amount": int(invoice.amount * 100),
        "currency": "INR",
        "receipt": f"INV-{invoice.id}",
    }

    order = client.order.create(order_data)

    return JsonResponse({
        "order_id": order["id"],
        "key": settings.RAZORPAY_KEY_ID,
        "amount": int(invoice.amount * 100),
        "customer": str(request.user),
        "invoice_id": invoice.id,  # returning actual ID
    })


# -----------------------------
# PAYMENT SUCCESS HANDLER
# -----------------------------
@login_required
def payment_success(request):
    invoice_id = request.GET.get("invoice_id")

    invoice = get_object_or_404(Invoice, pk=invoice_id, patient=request.user)

    invoice.status = "paid"
    invoice.save()

    return redirect("billing:billing-home")


# -----------------------------
# DOWNLOAD PDF INVOICE
# -----------------------------
@login_required
def download_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, patient=request.user)

    template = get_template("billing/invoice_pdf.html")
    html = template.render({"invoice": invoice})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="Invoice-{invoice.id}.pdf"'
    )

    pisa.CreatePDF(html, dest=response)
    return response
