
from django.db import models
from django.core.exceptions import ValidationError

class prodmast(models.Model):
    prodid = models.CharField(max_length=10, primary_key=True)
    prodname = models.CharField(max_length=100)
    price = models.FloatField()

    def clean(self):
        if self.price <= 0:
            raise ValidationError("Price must be a positive number.")

    def __str__(self):
        return f"{self.prodid} - {self.prodname}"

class stckmain(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Inbound'),
        ('OUT', 'Outbound'),
    ]
    stckid = models.AutoField(primary_key=True)
    trntype = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    billdt = models.DateField()
    totqty = models.IntegerField()

    def __str__(self):
        return f"{self.stckid} - {self.trntype} - {self.billdt}"

class stckdetail(models.Model):
    stckid = models.ForeignKey(stckmain, on_delete=models.CASCADE)
    prodid = models.ForeignKey(prodmast, on_delete=models.CASCADE)
    qty = models.IntegerField()

    def clean(self):
        if self.qty <= 0:
            raise ValidationError("Quantity must be greater than 0.")

        if self.stckid.trntype == 'OUT':
            from .utils import get_current_stock
            current = get_current_stock(self.prodid.prodid)
            if self.qty > current:
                raise ValidationError(
                    f"Cannot remove {self.qty} units. Only {current} in stock for product {self.prodid.prodid}."
                )

    def __str__(self):
        return f"{self.stckid} -> {self.prodid} ({self.qty})"
