from datetime import date

import pytest
from rest_framework.exceptions import ValidationError

from utils.date_parsers import parse_date_param


def test_parse_date_param_returns_date_for_valid_input():
    parsed = parse_date_param("2026-05-27", "start_date")

    assert parsed == date(2026, 5, 27)


@pytest.mark.parametrize("value", [None, "", "2026/05/27", "invalid-date"])
def test_parse_date_param_raises_validation_error_for_invalid_input(value):
    with pytest.raises(ValidationError) as exc_info:
        parse_date_param(value, "start_date")

    assert "start_date" in exc_info.value.detail
    assert "Informe uma data válida no formato YYYY-MM-DD." in str(exc_info.value)


def test_parse_date_param_uses_given_field_name_in_error():
    with pytest.raises(ValidationError) as exc_info:
        parse_date_param("bad", "end_date")

    assert "end_date" in exc_info.value.detail
