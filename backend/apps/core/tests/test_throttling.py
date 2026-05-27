import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.test import APIClient
from apps.core.views import CookieTokenObtainPairView


class LoginTestThrottle(SimpleRateThrottle):
    scope = 'login_test'

    def get_cache_key(self, request, view):
        return 'login-test-throttle-key'


def _create_user(username='throttle-user', password='Senha@123'):
    user_model = get_user_model()
    return user_model.objects.create_user(
        username=username,
        email=f'{username}@example.com',
        password=password,
    )


@pytest.fixture(autouse=True)
def _isolate_throttle_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.mark.django_db
def test_token_endpoint_blocks_with_429_after_login_rate_is_exceeded(monkeypatch):
    user = _create_user()
    payload = {'username': user.username, 'password': 'Senha@123'}
    client = APIClient()

    monkeypatch.setattr(LoginTestThrottle, 'THROTTLE_RATES', {'login_test': '2/min'})
    monkeypatch.setattr(CookieTokenObtainPairView, 'throttle_classes', [LoginTestThrottle])

    assert client.post('/api/v1/token/', payload, format='json').status_code == 200
    assert client.post('/api/v1/token/', payload, format='json').status_code == 200
    assert client.post('/api/v1/token/', payload, format='json').status_code == 429


@pytest.mark.django_db
def test_refresh_endpoint_not_blocked_by_login_throttle(monkeypatch):
    user = _create_user(username='refresh-user')
    payload = {'username': user.username, 'password': 'Senha@123'}
    client = APIClient()

    monkeypatch.setattr(LoginTestThrottle, 'THROTTLE_RATES', {'login_test': '1/min'})
    monkeypatch.setattr(CookieTokenObtainPairView, 'throttle_classes', [LoginTestThrottle])

    first = client.post('/api/v1/token/', payload, format='json')
    assert first.status_code == 200

    # Consume the login quota to ensure throttling happens only on /api/v1/token/.
    assert client.post('/api/v1/token/', payload, format='json').status_code == 429

    refresh_payload = {'refresh': first.cookies['refresh'].value}
    refresh_response = client.post('/api/v1/token/refresh/', refresh_payload, format='json')
    assert refresh_response.status_code == 200


@pytest.mark.django_db
def test_login_throttle_allows_requests_again_after_window(monkeypatch):
    user = _create_user(username='window-user')
    payload = {'username': user.username, 'password': 'Senha@123'}
    client = APIClient()
    now = [0.0]

    monkeypatch.setattr(LoginTestThrottle, 'THROTTLE_RATES', {'login_test': '1/min'})
    monkeypatch.setattr(LoginTestThrottle, 'timer', lambda _self: now[0])
    monkeypatch.setattr(CookieTokenObtainPairView, 'throttle_classes', [LoginTestThrottle])

    assert client.post('/api/v1/token/', payload, format='json').status_code == 200
    assert client.post('/api/v1/token/', payload, format='json').status_code == 429

    now[0] = 61.0
    assert client.post('/api/v1/token/', payload, format='json').status_code == 200
