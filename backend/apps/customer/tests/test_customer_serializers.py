import pytest
from apps.customer.serializers import (
    CustomerCreateUpdateSerializer,
    CustomerDetailSerializer,
    CustomerListSerializer,
)

from rest_framework.test import APIRequestFactory
from apps.customer.tests.factories import CustomerFactory


def make_request(user):
    factory = APIRequestFactory()
    req = factory.post('/')
    req.user = user
    return req


class DummyRequestUser:
    is_authenticated = True


class TestCustomerCreateUpdateSerializer:

    @pytest.mark.django_db
    def test_valid_data_creates_customer(self):
        data = {'name': 'João Silva', 'email': 'joao.silva@example.com'}
        s = CustomerCreateUpdateSerializer(data=data, context={'request': make_request(DummyRequestUser())})
        assert s.is_valid(), s.errors
        customer = s.save()
        assert customer.pk is not None
        assert customer.name == 'João Silva'

    def test_missing_name_is_invalid(self):
        data = {}
        s = CustomerCreateUpdateSerializer(data=data, context={'request': make_request(DummyRequestUser())})
        assert not s.is_valid()
        assert 'name' in s.errors


class TestCustomerDetailSerializer:

    def test_contains_expected_fields(self):
        c = CustomerFactory.build()
        s = CustomerDetailSerializer(c)
        for field in ['id', 'name', 'email', 'phone', 'created_at', 'updated_at']:
            assert field in s.data


class TestCustomerListSerializer:

    def test_contains_expected_fields(self):
        c = CustomerFactory.build()
        s = CustomerListSerializer(c)
        for field in ['id', 'name', 'email', 'phone', 'created_at', 'updated_at']:
            assert field in s.data
