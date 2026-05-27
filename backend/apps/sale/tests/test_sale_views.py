import json

import pytest

from apps.customer.tests.factories import CustomerFactory
from apps.product.tests.factories import ProductFactory
from apps.sale.models.sale import Sale
from apps.sale.tests.factories import SaleFactory
from apps.seller.tests.factories import SellerFactory


LIST_URL = '/api/sales/'


def DETAIL_URL(pk):
    return f'/api/sales/{pk}/'


class TestSaleAuthentication:

    def test_unauthenticated_returns_401(self, api_client):
        assert api_client.get(LIST_URL).status_code == 401


@pytest.mark.django_db
class TestSaleCRUD:

    def test_create_persists_sale(self, admin_client):
        customer = CustomerFactory()
        seller = SellerFactory()
        product = ProductFactory()
        data = {
            'invoice_number': 'INV-00001',
            'datetime': SaleFactory.build().datetime.isoformat(),
            'customer': customer.pk,
            'seller': seller.pk,
            'items': [
                {'product': product.pk, 'quantity': 2},
            ],
        }
        res = admin_client.post(LIST_URL, data, format='json')
        assert res.status_code == 201
        sale = Sale.objects.get(pk=res.data['id'])
        assert sale.invoice_number == 'INV-00001'
        assert sale.items.count() == 1

    def test_retrieve_uses_detail_serializer(self, admin_client):
        sale = SaleFactory()
        res = admin_client.get(DETAIL_URL(sale.pk))
        assert res.status_code == 200
        for field in ['id', 'invoice_number', 'datetime', 'customer', 'seller', 'items', 'total_value', 'total_commission', 'created_at']:
            assert field in res.data

    def test_list_uses_list_serializer(self, admin_client):
        SaleFactory()
        res = admin_client.get(LIST_URL)
        assert res.status_code == 200
        assert len(res.data['results']) == 1

    def test_partial_update_changes_invoice_number(self, admin_client):
        sale = SaleFactory(invoice_number='INV-00010')
        res = admin_client.patch(
            DETAIL_URL(sale.pk),
            json.dumps({'invoice_number': 'INV-00011'}),
            content_type='application/json',
        )
        assert res.status_code == 200
        sale.refresh_from_db()
        assert sale.invoice_number == 'INV-00011'

    def test_delete_performs_soft_delete(self, admin_client):
        sale = SaleFactory()
        res = admin_client.delete(DETAIL_URL(sale.pk))
        assert res.status_code == 204

        deleted = Sale.dm_objects.get(pk=sale.pk)
        assert deleted.deleted_at is not None
        assert not Sale.objects.filter(pk=sale.pk).exists()

    def test_retrieve_nonexistent_returns_404(self, admin_client):
        res = admin_client.get(DETAIL_URL('00000000-0000-0000-0000-000000000000'))
        assert res.status_code == 404

    def test_create_missing_invoice_number_returns_400(self, admin_client):
        sale = SaleFactory.build()
        product = ProductFactory()
        res = admin_client.post(LIST_URL, {
            'datetime': sale.datetime.isoformat(),
            'customer': sale.customer.pk,
            'seller': sale.seller.pk,
            'items': [
                {'product': product.pk, 'quantity': 1},
            ],
        })
        assert res.status_code == 400
        assert 'invoice_number' in res.data

    def test_create_missing_items_returns_400(self, admin_client):
        sale = SaleFactory.build()
        res = admin_client.post(LIST_URL, {
            'invoice_number': 'INV-00001',
            'datetime': sale.datetime.isoformat(),
            'customer': sale.customer.pk,
            'seller': sale.seller.pk,
        })
        assert res.status_code == 400
        assert 'items' in res.data


@pytest.mark.django_db
class TestSaleFilters:

    def test_search_by_invoice_number(self, admin_client):
        SaleFactory(invoice_number='INV-SEARCH-1')
        SaleFactory(invoice_number='INV-SEARCH-2')
        res = admin_client.get(LIST_URL, {'search': 'SEARCH-1'})
        assert res.status_code == 200
        assert res.data['count'] == 1
