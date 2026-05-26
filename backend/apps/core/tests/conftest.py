import pytest
from django.db import connection

from .factories import DummyPerson


@pytest.fixture(scope="session")
def dummy_person(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(DummyPerson)

        yield DummyPerson

        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(DummyPerson)
