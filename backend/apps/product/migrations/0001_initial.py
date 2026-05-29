import uuid
from decimal import Decimal

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.core.validators import MinValueValidator, MaxValueValidator


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True, default=None, null=True, verbose_name="Deleted at"
                    ),
                ),
                (
                    "code",
                    models.CharField(max_length=50, unique=True, verbose_name="Código"),
                ),
                (
                    "description",
                    models.CharField(max_length=255, verbose_name="Descrição"),
                ),
                (
                    "unit_value",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[MinValueValidator(Decimal("0.01"))],
                        verbose_name="Valor Unitário",
                    ),
                ),
                (
                    "commission_percentage",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=5,
                        validators=[
                            MinValueValidator(Decimal("0")),
                            MaxValueValidator(Decimal("10")),
                        ],
                        verbose_name="% Comissão",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_product_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_product_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "product",
                "ordering": ["code"],
                "verbose_name": "product",
                "verbose_name_plural": "products",
            },
        ),
    ]
