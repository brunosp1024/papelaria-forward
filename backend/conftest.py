import pytest

from types import SimpleNamespace
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return SimpleNamespace(
        is_authenticated=True,
        is_active=True,
        is_staff=True,
        pk=1,
        username="admin",
    )


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client
