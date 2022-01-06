from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class ItemModel(models.Model):
    tax_choices=(
        (0, '0%'),
        (1, '1%'),
        (5, '5%'),
        (10, '10%'),
    )
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    quantity=models.IntegerField()
    unit_price=models.FloatField()
    tax=models.IntegerField(choices=tax_choices)

class InvoiceModel(models.Model):
    invoice=models.FileField(upload_to="invoices")
    date_created=models.DateTimeField(auto_now_add=True, blank=True)