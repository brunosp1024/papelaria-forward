import json

import pytest

from apps.product.models import Product
from apps.product.tests.factories import ProductFactory


LIST_URL = '/api/products/'


def DETAIL_URL(pk):
    return f'/api/products/{pk}/'


class TestProductAuthentication:

    def test_unauthenticated_returns_401(self, api_client):
        assert api_client.get(LIST_URL).status_code == 401


@pytest.mark.django_db
class TestProductCRUD:

    def test_create_sets_default_not_deleted(self, admin_client):
        data = {
            'code': 'PROD-00001',
            'description': 'Notebook 14 polegadas',
            'unit_value': '99.90',
            'commission_percentage': '5.00',
        }
        res = admin_client.post(LIST_URL, data, format='json')
        assert res.status_code == 201
        assert Product.objects.get(pk=res.data['id']).deleted_at is None

    def test_retrieve_uses_detail_serializer(self, admin_client):
        product = ProductFactory()
        res = admin_client.get(DETAIL_URL(product.pk))
        assert res.status_code == 200
        for field in ['id', 'code', 'description', 'unit_value', 'commission_percentage', 'created_at', 'updated_at']:
            assert field in res.data

    def test_list_uses_list_serializer(self, admin_client):
        ProductFactory()
        res = admin_client.get(LIST_URL)
        assert res.status_code == 200
        assert len(res.data['results']) == 1

    def test_partial_update_changes_field(self, admin_client):
        product = ProductFactory(code='PROD-00001')
        res = admin_client.patch(
            DETAIL_URL(product.pk),
            json.dumps({'code': 'PROD-00002'}),
            content_type='application/json',
        )
        assert res.status_code == 200
        product.refresh_from_db()
        assert product.code == 'PROD-00002'

    def test_update_changes_multiple_fields(self, admin_client):
        product = ProductFactory(code='PROD-00001')
        payload = {
            'code': 'PROD-00002',
            'description': 'Novo produto',
            'unit_value': '129.90',
            'commission_percentage': '7.50',
        }
        res = admin_client.put(
            DETAIL_URL(product.pk),
            json.dumps(payload),
            content_type='application/json',
        )
        assert res.status_code == 200
        product.refresh_from_db()
        assert product.code == 'PROD-00002'
        assert product.description == 'Novo produto'
        assert str(product.unit_value) == '129.90'
        assert str(product.commission_percentage) == '7.50'

    def test_delete_performs_soft_delete(self, admin_client):
        product = ProductFactory()
        res = admin_client.delete(DETAIL_URL(product.pk))
        assert res.status_code == 204

        deleted = Product.dm_objects.get(pk=product.pk)
        assert deleted.deleted_at is not None
        assert not Product.objects.filter(pk=product.pk).exists()

    def test_retrieve_nonexistent_returns_404(self, admin_client):
        res = admin_client.get(DETAIL_URL('00000000-0000-0000-0000-000000000000'))
        assert res.status_code == 404

    def test_create_missing_code_returns_400(self, admin_client):
        res = admin_client.post(LIST_URL, {'description': 'Produto sem código', 'unit_value': '9.90', 'commission_percentage': '1.00'})
        assert res.status_code == 400
        assert 'code' in res.data

    def test_create_duplicate_code_returns_400(self, admin_client):
        ProductFactory(code='PROD-99999')
        res = admin_client.post(
            LIST_URL,
            {
                'code': 'PROD-99999',
                'description': 'Notebook',
                'unit_value': '99.90',
                'commission_percentage': '3.00',
            },
        )
        assert res.status_code == 400
        assert 'code' in res.data


@pytest.mark.django_db
class TestProductFilters:

    def test_search_by_description(self, admin_client):
        ProductFactory(code='PROD-10001', description='Caderno Pro')
        ProductFactory(code='PROD-10002', description='Caneta Azul')
        res = admin_client.get(LIST_URL, {'search': 'Caderno'})
        assert res.status_code == 200
        assert res.data['count'] == 1

    def test_search_by_code(self, admin_client):
        ProductFactory(code='PROD-TEST-01')
        ProductFactory(code='PROD-TEST-02')
        res = admin_client.get(LIST_URL, {'search': 'TEST-01'})
        assert res.status_code == 200
        assert res.data['count'] == 1
