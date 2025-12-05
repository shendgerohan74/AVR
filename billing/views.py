import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa
import razorpay
from .models import Invoice


# -----------------------------
# BILLING HOME PAGE
# -----------------------------
@login_required
def billing_home(request):
    print("✅ USING BILLING HOME VIEW")

    patient = request.user.patientprofile

    pending = Invoice.objects.filter(patient=patient, status="issued")
    history = Invoice.objects.filter(patient=patient, status="paid")

    print("\n================ DEBUG BILLING ================")
    print("LOGGED USER:", request.user, request.user.email)
    print("PATIENT PROFILE:", patient)
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

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def create_order(request, invoice_id):
    patient = request.user.patientprofile  # ✅ FIXED

    invoice = Invoice.objects.get(id=invoice_id, patient=patient)  # ✅ FIXED

    amount = int(invoice.amount * 100)  # ✅ Razorpay expects paise

    order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1,
    })

    return JsonResponse({
        "key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "order_id": order["id"]
    })

# -----------------------------
# PAYMENT SUCCESS HANDLER
# -----------------------------
@login_required
def payment_success(request):
    invoice_id = request.GET.get("invoice_id")

    invoice = get_object_or_404(Invoice, pk=invoice_id, patient=request.user.patientprofile)

    invoice.status = "paid"
    invoice.save()

    return redirect("billing:billing-home")


# -----------------------------
# DOWNLOAD PDF INVOICE
# -----------------------------
@login_required
def download_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, patient=request.user.patientprofile)

    template = get_template("billing/invoice_pdf.html")
    html = template.render({"invoice": invoice})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="Invoice-{invoice.id}.pdf"'
    )

    pisa.CreatePDF(html, dest=response)
    return response
