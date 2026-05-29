from django.utils.dateparse import parse_date
from rest_framework.exceptions import ValidationError


def parse_date_param(value, field_name):
    parsed_date = parse_date(value or "")

    if parsed_date is None:
        raise ValidationError(
            {field_name: "Informe uma data válida no formato YYYY-MM-DD."}
        )

    return parsed_date
