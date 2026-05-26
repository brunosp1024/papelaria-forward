import json

import pytest
from apps.customer.models import Customer
from apps.customer.tests.factories import CustomerFactory


LIST_URL = '/api/customers/'


def DETAIL_URL(pk):
    return f'/api/customers/{pk}/'

class TestCustomerAuthentication:

    def test_unauthenticated_returns_401(self, api_client):
        assert api_client.get(LIST_URL).status_code == 401


@pytest.mark.django_db
class TestCustomerCRUD:

    def test_create_sets_default_is_active(self, admin_client):
        data = {'name': 'New Customer', 'email': 'new-customer@example.com'}
        res = admin_client.post(LIST_URL, data, format='json')
        assert res.status_code == 201
        assert Customer.objects.get(pk=res.data['id']).deleted_at is None

    def test_retrieve_uses_detail_serializer(self, admin_client):
        c = CustomerFactory()
        res = admin_client.get(DETAIL_URL(c.pk))
        assert res.status_code == 200
        for field in ['id', 'name', 'created_at', 'updated_at']:
            assert field in res.data

    def test_list_uses_list_serializer(self, admin_client):
        CustomerFactory()
        res = admin_client.get(LIST_URL)
        assert res.status_code == 200

    def test_partial_update_changes_field(self, admin_client):
        c = CustomerFactory(name='Old Name')
        res = admin_client.patch(
            DETAIL_URL(c.pk),
            json.dumps({'name': 'New Name'}),
            content_type='application/json',
        )
        assert res.status_code == 200
        c.refresh_from_db()
        assert c.name == 'New Name'

    def test_update_changes_multiple_fields(self, admin_client):
        c = CustomerFactory(name='Old Name', email='old@example.com')
        payload = {'name': 'New Name', 'email': 'new@example.com', 'phone': '11999990000'}
        res = admin_client.put(
            DETAIL_URL(c.pk),
            json.dumps(payload),
            content_type='application/json',
        )
        assert res.status_code == 200
        c.refresh_from_db()
        assert c.name == 'New Name'
        assert c.email == 'new@example.com'
        assert c.phone == '11999990000'

    def test_delete_performs_soft_delete(self, admin_client):
        c = CustomerFactory()
        res = admin_client.delete(DETAIL_URL(c.pk))
        assert res.status_code == 204

        deleted = Customer.dm_objects.get(pk=c.pk)
        assert deleted.deleted_at is not None
        assert not Customer.objects.filter(pk=c.pk).exists()

    def test_retrieve_nonexistent_returns_404(self, admin_client):
        res = admin_client.get(DETAIL_URL('00000000-0000-0000-0000-000000000000'))
        assert res.status_code == 404

    def test_create_missing_name_returns_400(self, admin_client):
        res = admin_client.post(LIST_URL, {'email': 'test@example.com'})
        assert res.status_code == 400
        assert 'name' in res.data

    def test_create_duplicate_email_returns_400(self, admin_client):
        CustomerFactory(email='duplicate@example.com')
        res = admin_client.post(LIST_URL, {'name': 'New Customer', 'email': 'duplicate@example.com'})
        assert res.status_code == 400
        assert 'email' in res.data


@pytest.mark.django_db
class TestCustomerFilters:

    def test_search_by_name(self, admin_client):
        CustomerFactory(name='Zacarias Provider')
        CustomerFactory(name='Maria Customer')
        res = admin_client.get(LIST_URL, {'search': 'Zacarias'})
        assert res.status_code == 200
        assert res.data['count'] == 1

    def test_search_by_email(self, admin_client):
        CustomerFactory(email='test@example.com')
        CustomerFactory(email='another@example.com')
        res = admin_client.get(LIST_URL, {'search': 'test'})
        assert res.status_code == 200
        assert res.data['count'] == 1
