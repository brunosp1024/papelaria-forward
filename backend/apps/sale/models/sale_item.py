from django.db import models
from django.core.validators import MinValueValidator

from apps.product.models import Product
from apps.core.models.mixins import BaseModel
from apps.sale.models.sale import Sale
from apps.sale.models.commission_config import CommissionConfig


class SaleItem(BaseModel):
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE, related_name="items", verbose_name="Venda"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, verbose_name="Produto"
    )
    quantity = models.PositiveIntegerField(
        "Quantidade", validators=[MinValueValidator(1)]
    )

    class Meta:
        verbose_name = "Item da Venda"
        verbose_name_plural = "Itens da Venda"

    def __str__(self):
        return f"{self.product.code} x{self.quantity}"

    @property
    def subtotal(self):
        return self.product.unit_value * self.quantity

    @property
    def commission_value(self):
        """Aplica regras de min/max por dia da semana."""
        percentage = self.product.commission_percentage
        weekday = self.sale.datetime.weekday()

        try:
            config = CommissionConfig.objects.get(day_of_week=weekday)
            percentage = max(
                config.min_percentage, min(percentage, config.max_percentage)
            )
        except CommissionConfig.DoesNotExist:
            pass

        return (percentage / 100) * self.subtotal
