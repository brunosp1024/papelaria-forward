from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from apps.core.models.mixins import BaseModel


class CommissionConfig(BaseModel):
    """Configuração de comissão por dia da semana (configurável)."""

    WEEKDAYS = [
        (0, "Segunda-feira"),
        (1, "Terça-feira"),
        (2, "Quarta-feira"),
        (3, "Quinta-feira"),
        (4, "Sexta-feira"),
        (5, "Sábado"),
        (6, "Domingo"),
    ]
    day_of_week = models.IntegerField("Dia da Semana", choices=WEEKDAYS, unique=True)
    min_percentage = models.DecimalField(
        "% Mínima",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("10"))],
    )
    max_percentage = models.DecimalField(
        "% Máxima",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("10"))],
    )

    class Meta:
        db_table = "commission_config"
        verbose_name = "Commission Config"
        verbose_name_plural = "Commission Configs"
        ordering = ["day_of_week"]

    def __str__(self):
        return f"{self.get_day_of_week_display()} ({self.min_percentage}% - {self.max_percentage}%)"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.min_percentage > self.max_percentage:
            raise ValidationError("O mínimo não pode ser maior que o máximo.")
