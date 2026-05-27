import pytest


@pytest.fixture
def obj(db, dummy_person):
    return dummy_person.dm_objects.create(name="Test")


def test_soft_delete_sets_deleted_at(obj):
    obj.delete()
    obj.refresh_from_db(from_queryset=obj.__class__.dm_objects.all())
    assert obj.deleted_at is not None


def test_soft_delete_keeps_in_database(obj, dummy_person):
    obj.delete()
    assert dummy_person.dm_objects.filter(pk=obj.pk).exists()


def test_soft_deleted_hidden_from_default_manager(obj, dummy_person):
    obj.delete()
    assert not dummy_person.objects.filter(pk=obj.pk).exists()


def test_dm_objects_returns_deleted(obj, dummy_person):
    obj.delete()
    assert dummy_person.dm_objects.filter(pk=obj.pk).exists()


def test_hard_delete_removes_from_database(obj, dummy_person):
    obj.hard_delete()
    assert not dummy_person.dm_objects.filter(pk=obj.pk).exists()
