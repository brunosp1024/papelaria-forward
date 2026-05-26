from django.db import models

from backend.utils.validators import validate_phone
from .mixins import BaseModel


class Person(BaseModel):
    """Abstract model shared by other models."""
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True, validators=[validate_phone])

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
