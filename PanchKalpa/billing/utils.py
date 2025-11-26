def generate_invoice_id():
    from datetime import datetime
    from billing.models import Invoice

    year = datetime.now().year
    count = Invoice.objects.filter(created_at__year=year).count() + 1
    return f"INV-{year}-{count:04d}"
