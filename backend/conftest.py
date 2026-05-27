import pytest
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope="session")
def admin_user(django_db_setup, django_db_blocker):
    user_model = get_user_model()
    with django_db_blocker.unblock():
        user, _ = user_model.objects.get_or_create(
            username="admin",
            defaults={
                "is_staff": True,
                "is_active": True,
            },
        )
    return user


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client
