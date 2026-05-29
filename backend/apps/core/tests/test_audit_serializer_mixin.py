import pytest
from rest_framework.test import APIRequestFactory

from apps.core.serializers.audit_serializer_mixin import AuditSerializerMixin
from apps.customer.models import Customer


class DummyAuditSerializer(AuditSerializerMixin):
    class Meta:
        model = Customer
        fields = ["id", "name", "email", "phone", "created_by", "updated_by"]
        read_only_fields = ["created_by", "updated_by"]


def make_request(user):
    factory = APIRequestFactory()
    req = factory.post("/")
    req.user = user
    return req


@pytest.mark.django_db
class TestAuditSerializerMixin:
    def test_created_by_and_updated_by_are_set_on_create(self, admin_user):
        serializer = DummyAuditSerializer(
            data={"name": "Audit Test", "email": "audit-create@example.com"},
            context={"request": make_request(admin_user)},
        )
        assert serializer.is_valid(), serializer.errors
        obj = serializer.save()
        assert obj.created_by == admin_user
        assert obj.updated_by == admin_user

    def test_updated_by_is_set_on_update(self, django_user_model):
        update_user = django_user_model.objects.create_user(username="user-update")
        obj = Customer.objects.create(name="Original", email="original@example.com")
        assert obj.created_by is None
        serializer = DummyAuditSerializer(
            obj,
            data={"name": "Updated"},
            partial=True,
            context={"request": make_request(update_user)},
        )
        assert serializer.is_valid(), serializer.errors
        serializer.save()
        obj.refresh_from_db()
        assert obj.updated_by == update_user

    def test_created_by_and_updated_by_without_user(self):
        """Test that created_by and updated_by are None when no user is provided."""
        serializer = DummyAuditSerializer(
            data={"name": "Audit Test", "email": "audit-without-user@example.com"},
            context={"request": None},
        )
        assert serializer.is_valid(), serializer.errors
        obj = serializer.save()
        assert obj.created_by is None
        assert obj.updated_by is None
