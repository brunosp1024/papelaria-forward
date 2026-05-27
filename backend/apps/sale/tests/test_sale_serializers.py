import pytest
from rest_framework.test import APIRequestFactory

from apps.sale.serializers import (
    SaleReadSerializer,
    SaleWriteSerializer,
)
from apps.sale.models.sale_item import SaleItem
from apps.sale.tests.factories import SaleFactory
from apps.customer.tests.factories import CustomerFactory
from apps.product.tests.factories import ProductFactory
from apps.seller.tests.factories import SellerFactory


def make_request(user):
    factory = APIRequestFactory()
    req = factory.post('/')
    req.user = user
    return req


class TestSaleWriteSerializer:

    @pytest.mark.django_db
    def test_valid_data_creates_sale(self, admin_user):
        customer = CustomerFactory()
        seller = SellerFactory()
        product = ProductFactory()
        data = {
            'invoice_number': 'INV-00001',
            'datetime': '2026-05-26T12:00:00Z',
            'customer': customer.pk,
            'seller': seller.pk,
            'items': [
                {'product': product.pk, 'quantity': 2},
            ],
        }
        s = SaleWriteSerializer(data=data, context={'request': make_request(admin_user)})
        assert s.is_valid(), s.errors
        sale = s.save()
        assert sale.pk is not None
        assert sale.invoice_number == 'INV-00001'
        assert sale.items.count() == 1
        assert sale.created_by == admin_user
        assert sale.updated_by == admin_user

    @pytest.mark.django_db
    def test_missing_invoice_number_is_invalid(self):
        customer = CustomerFactory()
        seller = SellerFactory()
        product = ProductFactory()
        data = {
            'datetime': '2026-05-26T12:00:00Z',
            'customer': customer.pk,
            'seller': seller.pk,
            'items': [
                {'product': product.pk, 'quantity': 1},
            ],
        }
        s = SaleWriteSerializer(data=data)
        assert not s.is_valid()
        assert 'invoice_number' in s.errors

    @pytest.mark.django_db
    def test_missing_items_is_invalid(self):
        customer = CustomerFactory()
        seller = SellerFactory()
        s = SaleWriteSerializer(data={
            'invoice_number': 'INV-00001',
            'datetime': '2026-05-26T12:00:00Z',
            'customer': customer.pk,
            'seller': seller.pk,
        })
        assert not s.is_valid()
        assert 'items' in s.errors

    @pytest.mark.django_db
    def test_empty_items_is_invalid(self):
        customer = CustomerFactory()
        seller = SellerFactory()
        s = SaleWriteSerializer(data={
            'invoice_number': 'INV-00001',
            'datetime': '2026-05-26T12:00:00Z',
            'customer': customer.pk,
            'seller': seller.pk,
            'items': [],
        })

        assert not s.is_valid()
        assert 'items' in s.errors

    @pytest.mark.django_db
    def test_update_replaces_existing_items(self, admin_user):
        sale = SaleFactory(invoice_number='INV-00001')
        original_product = ProductFactory(code='PROD-OLD')
        replacement_product = ProductFactory(code='PROD-NEW')
        SaleItem.objects.create(sale=sale, product=original_product, quantity=1)

        s = SaleWriteSerializer(
            instance=sale,
            data={
                'invoice_number': 'INV-00001',
                'datetime': sale.datetime.isoformat(),
                'customer': sale.customer.pk,
                'seller': sale.seller.pk,
                'items': [
                    {'product': replacement_product.pk, 'quantity': 3},
                ],
            },
            context={'request': make_request(admin_user)},
        )
        assert s.is_valid(), s.errors
        updated_sale = s.save()

        assert updated_sale.items.count() == 1
        updated_item = updated_sale.items.first()
        assert updated_item.product_id == replacement_product.pk
        assert updated_item.quantity == 3
        assert updated_sale.updated_by == admin_user

    @pytest.mark.django_db
    def test_create_without_authenticated_user_keeps_audit_fields_null(self):
        customer = CustomerFactory()
        seller = SellerFactory()
        product = ProductFactory()
        data = {
            'invoice_number': 'INV-00002',
            'datetime': '2026-05-26T12:00:00Z',
            'customer': customer.pk,
            'seller': seller.pk,
            'items': [
                {'product': product.pk, 'quantity': 1},
            ],
        }
        s = SaleWriteSerializer(data=data, context={'request': None})
        assert s.is_valid(), s.errors
        sale = s.save()
        assert sale.created_by is None
        assert sale.updated_by is None


class TestSaleReadSerializer:

    @pytest.mark.django_db
    def test_contains_expected_fields(self):
        sale = SaleFactory.build()
        s = SaleReadSerializer(sale)
        for field in [
            'id', 'invoice_number', 'datetime', 'customer', 'seller', 'items',
            'total_value', 'total_commission', 'created_at'
        ]:
            assert field in s.data
