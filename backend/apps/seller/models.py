from django.db import models

from apps.core.models.person import Person


class Seller(Person):
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = "sellers"
        ordering = ["-created_at"]
        verbose_name = "Seller"
        verbose_name_plural = "Sellers"
