import re
from rest_framework.exceptions import ValidationError


def validate_phone(value: str) -> None:
    if not value:
        return

    phone = re.sub(r"[\s\-\(\)\+]", "", value)

    if not phone.isdigit():
        raise ValidationError("Telefone deve conter apenas dígitos.")

    if len(phone) not in (10, 11):
        raise ValidationError("Telefone deve ter 10 ou 11 dígitos (com DDD).")
