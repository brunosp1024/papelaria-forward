import pytest
from django.db import connection

from apps.sale.models.commission_config import CommissionConfig
from apps.sale.models.sale import Sale
from apps.sale.models.sale_item import SaleItem


@pytest.fixture(scope="session", autouse=True)
def ensure_sale_tables(django_db_setup, django_db_blocker):
    models = [Sale, CommissionConfig, SaleItem]

    with django_db_blocker.unblock():
        existing_tables = set(connection.introspection.table_names())
        created_models = [m for m in models if m._meta.db_table not in existing_tables]

        if created_models:
            with connection.schema_editor() as schema_editor:
                for model in created_models:
                    schema_editor.create_model(model)

    yield

    with django_db_blocker.unblock():
        if created_models:
            with connection.schema_editor() as schema_editor:
                for model in reversed(created_models):
                    schema_editor.delete_model(model)
