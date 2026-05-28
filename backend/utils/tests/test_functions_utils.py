import pytest
from utils.functions_utils import generate_random_code


# Test: generated code has correct length
def test_generate_random_code_length():
    code = generate_random_code(9)
    assert len(code) == 9
    assert code.isdigit()

# Test: generated code with custom length
def test_generate_random_code_custom_length():
    code = generate_random_code(5)
    assert len(code) == 5
    assert code.isdigit()

# Test: length < 1 raises ValueError
def test_generate_random_code_invalid_length():
    with pytest.raises(ValueError):
        generate_random_code(0)
    with pytest.raises(ValueError):
        generate_random_code(-3)

# Test: generated codes are random
def test_generate_random_code_randomness():
    codes = {generate_random_code() for _ in range(10)}
    assert len(codes) == 10
