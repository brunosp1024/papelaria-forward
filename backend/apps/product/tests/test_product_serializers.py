import pytest
from rest_framework.test import APIRequestFactory

from apps.product.serializers import (
    ProductCreateUpdateSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)
from apps.product.tests.factories import ProductFactory


def make_request(user):
    factory = APIRequestFactory()
    req = factory.post("/")
    req.user = user
    return req


class TestProductCreateUpdateSerializer:
    @pytest.mark.django_db
    def test_valid_data_creates_product(self):
        data = {
            "code": "PROD-00001",
            "description": "Notebook 14 polegadas",
            "unit_value": "99.90",
            "commission_percentage": "5.00",
        }
        s = ProductCreateUpdateSerializer(data=data)
        assert s.is_valid(), s.errors
        product = s.save()
        assert product.pk is not None
        assert product.code == "PROD-00001"

    def test_missing_code_is_invalid(self):
        data = {}
        s = ProductCreateUpdateSerializer(data=data)
        assert not s.is_valid()
        assert "code" in s.errors


class TestProductDetailSerializer:
    def test_contains_expected_fields(self):
        s = ProductDetailSerializer(ProductFactory.build())
        for field in [
            "id",
            "code",
            "description",
            "unit_value",
            "commission_percentage",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]:
            assert field in s.data


class TestProductListSerializer:
    def test_contains_expected_fields(self):
        s = ProductListSerializer(ProductFactory.build())
        for field in [
            "id",
            "code",
            "description",
            "unit_value",
            "commission_percentage",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]:
            assert field in s.data
