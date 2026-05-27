import json

import pytest

from apps.seller.models import Seller
from apps.seller.tests.factories import SellerFactory


LIST_URL = '/api/v1/sellers/'


def DETAIL_URL(pk):
    return f'/api/v1/sellers/{pk}/'


class TestSellerAuthentication:

    def test_unauthenticated_returns_401(self, api_client):
        assert api_client.get(LIST_URL).status_code == 401


@pytest.mark.django_db
class TestSellerCRUD:

    def test_create_sets_default_not_deleted(self, admin_client):
        data = {'name': 'New Seller', 'email': 'new-seller@example.com'}
        res = admin_client.post(LIST_URL, data, format='json')
        assert res.status_code == 201
        assert Seller.objects.get(pk=res.data['id']).deleted_at is None

    def test_retrieve_uses_detail_serializer(self, admin_client):
        seller = SellerFactory()
        res = admin_client.get(DETAIL_URL(seller.pk))
        assert res.status_code == 200
        for field in ['id', 'name', 'created_at', 'updated_at']:
            assert field in res.data

    def test_list_uses_list_serializer(self, admin_client):
        SellerFactory()
        res = admin_client.get(LIST_URL)
        assert res.status_code == 200
        assert "count" in res.data
        assert "results" in res.data
        assert len(res.data["results"]) == 1

    def test_partial_update_changes_field(self, admin_client):
        seller = SellerFactory(name='Old Name')
        res = admin_client.patch(
            DETAIL_URL(seller.pk),
            json.dumps({'name': 'New Name'}),
            content_type='application/json',
        )
        assert res.status_code == 200
        seller.refresh_from_db()
        assert seller.name == 'New Name'

    def test_update_changes_multiple_fields(self, admin_client):
        seller = SellerFactory(name='Old Name', email='old@example.com')
        payload = {'name': 'New Name', 'email': 'new@example.com', 'phone': '11999990000'}
        res = admin_client.put(
            DETAIL_URL(seller.pk),
            json.dumps(payload),
            content_type='application/json',
        )
        assert res.status_code == 200
        seller.refresh_from_db()
        assert seller.name == 'New Name'
        assert seller.email == 'new@example.com'
        assert seller.phone == '11999990000'

    def test_delete_performs_soft_delete(self, admin_client):
        seller = SellerFactory()
        res = admin_client.delete(DETAIL_URL(seller.pk))
        assert res.status_code == 204

        deleted = Seller.dm_objects.get(pk=seller.pk)
        assert deleted.deleted_at is not None
        assert not Seller.objects.filter(pk=seller.pk).exists()

    def test_retrieve_nonexistent_returns_404(self, admin_client):
        res = admin_client.get(DETAIL_URL('00000000-0000-0000-0000-000000000000'))
        assert res.status_code == 404

    def test_create_missing_name_returns_400(self, admin_client):
        res = admin_client.post(LIST_URL, {'email': 'test@example.com'})
        assert res.status_code == 400
        assert 'name' in res.data

    def test_create_duplicate_email_returns_400(self, admin_client):
        SellerFactory(email='duplicate@example.com')
        res = admin_client.post(LIST_URL, {'name': 'New Seller', 'email': 'duplicate@example.com'})
        assert res.status_code == 400
        assert 'email' in res.data


@pytest.mark.django_db
class TestSellerFilters:

    def test_search_by_name(self, admin_client):
        SellerFactory(name='Zacarias Seller')
        SellerFactory(name='Maria Seller')
        res = admin_client.get(LIST_URL, {'search': 'Zacarias'})
        assert res.status_code == 200
        assert res.data['count'] == 1

    def test_search_by_email(self, admin_client):
        SellerFactory(email='test@example.com')
        SellerFactory(email='another@example.com')
        res = admin_client.get(LIST_URL, {'search': 'test'})
        assert res.status_code == 200
        assert res.data['count'] == 1
