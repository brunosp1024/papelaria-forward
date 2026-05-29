from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.core.models.mixins import BaseModel


class Product(BaseModel):
    code = models.CharField("Código", max_length=50, unique=True)
    description = models.CharField("Descrição", max_length=255)
    unit_value = models.DecimalField(
        "Valor Unitário",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    commission_percentage = models.DecimalField(
        "% Comissão",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("10"))],
    )

    class Meta:
        db_table = "product"
        ordering = ["code"]
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return f"{self.code} - {self.description}"
