from django.db import models

from apps.core.models.mixins import BaseModel


class DummyPerson(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)

    class Meta:
        app_label = "core"
