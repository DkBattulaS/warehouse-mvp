# inventory/utils.py
from .models import stckdetail
from django.db.models import Sum

def get_current_stock(product_id):
    inbound = stckdetail.objects.filter(
        prodid_id=product_id,
        stckid__trntype__iexact='IN'
    ).aggregate(total=Sum('qty'))['total'] or 0

    outbound = stckdetail.objects.filter(
        prodid_id=product_id,
        stckid__trntype__iexact='OUT'
    ).aggregate(total=Sum('qty'))['total'] or 0

    return inbound - outbound
