import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from apps.seller.serializers import (
    SellerCreateUpdateSerializer,
    SellerDetailSerializer,
    SellerListSerializer,
)
from apps.seller.tests.factories import SellerFactory


def make_request(user):
    factory = APIRequestFactory()
    req = factory.post('/')
    req.user = user
    return req


class TestSellerCreateUpdateSerializer:

    @pytest.mark.django_db
    def test_valid_data_creates_seller(self):
        user = get_user_model().objects.create_user(username='seller-serializer-user')
        data = {'name': 'Joao Silva', 'email': 'joao.silva@example.com'}
        s = SellerCreateUpdateSerializer(data=data, context={'request': make_request(user)})
        assert s.is_valid(), s.errors
        seller = s.save()
        assert seller.pk is not None
        assert seller.name == 'Joao Silva'

    def test_missing_name_is_invalid(self):
        data = {}
        s = SellerCreateUpdateSerializer(data=data, context={'request': None})
        assert not s.is_valid()
        assert 'name' in s.errors


class TestSellerDetailSerializer:

    def test_contains_expected_fields(self):
        s = SellerDetailSerializer(SellerFactory.build())
        for field in [
            'id', 'name', 'email', 'phone', 'created_at',
            'updated_at', 'created_by', 'updated_by'
        ]:
            assert field in s.data


class TestSellerListSerializer:

    def test_contains_expected_fields(self):
        s = SellerListSerializer(SellerFactory.build())
        for field in [
            'id', 'name', 'email', 'phone', 'created_at',
            'updated_at', 'created_by', 'updated_by'
        ]:
            assert field in s.data
