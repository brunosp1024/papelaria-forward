import pytest
from rest_framework.exceptions import ValidationError

from utils.validators import validate_phone


def test_validate_phone_accepts_empty_values():
    assert validate_phone(None) is None
    assert validate_phone("") is None


def test_validate_phone_accepts_valid_format():
    assert validate_phone("(11) 98765-4321") is None


def test_validate_phone_accepts_10_digits_with_ddd():
	assert validate_phone("1132345678") is None


def test_validate_phone_accepts_11_digits_with_ddd():
	assert validate_phone("11912345678") is None


def test_validate_phone_rejects_non_digit_chars():
    with pytest.raises(ValidationError) as exc_info:
        validate_phone("11A98765432")
    assert "Telefone deve conter apenas dígitos." in str(exc_info.value)


def test_validate_phone_rejects_invalid_length():
    with pytest.raises(ValidationError) as exc_info:
        validate_phone("119876")
    assert "Telefone deve ter 10 ou 11 dígitos (com DDD)." in str(exc_info.value)
