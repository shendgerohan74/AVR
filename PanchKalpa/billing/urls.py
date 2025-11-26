from django.urls import path
from . import views

app_name = "billing"

urlpatterns = [
    path("", views.billing_home, name="billing-home"),
    path("order/<int:invoice_id>/", views.create_order, name="create-order"),
    path("success/", views.payment_success, name="payment-success"),
    path("download/<str:invoice_id>/", views.download_invoice, name="download-invoice"),
]
