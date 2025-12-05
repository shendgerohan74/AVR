from django.contrib import admin
from . import models
from .models import Invoice, Payment

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "patient", "amount", "status", "due_date", "created_at")
    list_filter = ("status", )
    search_fields = ("patient__username", "patient__email")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "invoice", "gateway", "gateway_order_id", "gateway_payment_id", "amount", "status", "created_at")
    list_filter = ("gateway", "status")
    search_fields = ("gateway_order_id", "gateway_payment_id", "invoice__id")
