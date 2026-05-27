from django.db import models

from apps.core.models.mixins import BaseModel
from apps.customer.models import Customer
from apps.seller.models import Seller


class Sale(BaseModel):
    invoice_number = models.CharField('Invoice number', max_length=50, unique=True)
    datetime = models.DateTimeField('Datetime')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales')
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, related_name='sales')

    class Meta:
        db_table = 'sales'
        ordering = ['-datetime']
        verbose_name = 'sale'
        verbose_name_plural = 'sales'

    def __str__(self):
        return f"NF {self.invoice_number}"

    @property
    def total_value(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_commission(self):
        return sum(item.commission_value for item in self.items.all())
