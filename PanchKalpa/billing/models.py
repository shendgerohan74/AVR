from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL





class Invoice(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("issued", "Issued"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invoices")
    invoice_id = models.CharField(max_length=30, unique=True, default="temp")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="issued")

    # optional link to appointment (if you want)
    appointment = models.ForeignKey("Patient.Appointment", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Invoice #{self.id} — {self.patient} — {self.amount}"

class Payment(models.Model):
    GATEWAY_CHOICES = [
        ("razorpay", "Razorpay"),
        ("stripe", "Stripe"),
    ]
    STATUS_CHOICES = [
        ("created", "Created"),
        ("success", "Success"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments")
    gateway = models.CharField(max_length=30, choices=GATEWAY_CHOICES)
    gateway_order_id = models.CharField(max_length=255, blank=True, null=True)
    gateway_payment_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created")
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Payment {self.id} — {self.gateway} — {self.status}"
