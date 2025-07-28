# inventory/views.py
from django.shortcuts import render
from .models import prodmast
from .utils import get_current_stock

def inventory_view(request):
    products = prodmast.objects.all()
    inventory = []
    for p in products:
        inventory.append({
            'name': p.prodname,
            'sku': p.prodid,
            'stock': get_current_stock(p.prodid)
        })
    return render(request, 'inventory/inventory.html', {'inventory': inventory})
