import pytest


from apps.core.serializers.serializers import PersonSerializer
from .factories import DummyPerson


class DummyPersonSerializer(PersonSerializer):
    class Meta:
        model = DummyPerson
        fields = ["id", "name", "email", "phone"]


@pytest.mark.django_db
class TestPersonSerializer:
    def test_duplicate_phone_is_rejected(self, dummy_person):
        dummy_person.objects.create(
            name="Pessoa 1", email="pessoa1@example.com", phone="11912345678"
        )
        serializer = DummyPersonSerializer(
            data={
                "name": "Pessoa 2",
                "email": "pessoa2@example.com",
                "phone": "11912345678",
            }
        )
        assert not serializer.is_valid()
        assert "phone" in serializer.errors

    def test_invalid_phone_is_rejected(self, dummy_person):
        serializer = DummyPersonSerializer(
            data={"name": "Pessoa 3", "email": "pessoa3@example.com", "phone": "abc123"}
        )
        assert not serializer.is_valid()
        assert "phone" in serializer.errors

    def test_blank_phone_is_optional(self, dummy_person):
        serializer = DummyPersonSerializer(
            data={"name": "Pessoa 4", "email": "pessoa4@example.com", "phone": ""}
        )
        assert serializer.is_valid(), serializer.errors
        person = serializer.save()
        assert person.phone is None

    def test_duplicate_phone_allows_editing_same_record(self, dummy_person):
        person = dummy_person.objects.create(
            name="Pessoa 5", email="pessoa5@example.com", phone="11912345678"
        )
        serializer = DummyPersonSerializer(
            person,
            data={
                "name": "Pessoa 5 Atualizada",
                "email": "pessoa5@example.com",
                "phone": "11912345678",
            },
        )
        assert serializer.is_valid(), serializer.errors
