import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestJWTAuthentication:

    @pytest.fixture(autouse=True)
    def _disable_auth_throttle(self, settings):
        settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["auth"] = "1000/minute"

    def test_obtain_token_sets_jwt_cookies(self, django_user_model):
        django_user_model.objects.create_user(username="jwt-user", password="jwt-pass")
        client = APIClient()

        res = client.post(
            "/api/v1/token/",
            {"username": "jwt-user", "password": "jwt-pass"},
            format="json",
        )

        assert res.status_code == 200
        assert res.data["detail"] == "Login successful."
        assert "access" in res.cookies
        assert "refresh" in res.cookies

    def test_access_protected_endpoint_with_bearer_token(self, django_user_model):
        django_user_model.objects.create_user(username="jwt-user-2", password="jwt-pass-2")
        client = APIClient()

        token_res = client.post(
            "/api/v1/token/",
            {"username": "jwt-user-2", "password": "jwt-pass-2"},
            format="json",
        )
        assert token_res.status_code == 200

        access_token = token_res.cookies["access"].value
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        protected_res = client.get("/api/v1/customers/")

        assert protected_res.status_code == 200

    def test_access_protected_endpoint_with_access_cookie(self, django_user_model):
        django_user_model.objects.create_user(username="jwt-user-cookie-2", password="jwt-pass-cookie-2")
        client = APIClient()

        token_res = client.post(
            "/api/v1/token/",
            {"username": "jwt-user-cookie-2", "password": "jwt-pass-cookie-2"},
            format="json",
        )
        assert token_res.status_code == 200

        protected_res = client.get("/api/v1/customers/")

        assert protected_res.status_code == 200

    def test_refresh_uses_refresh_cookie(self, django_user_model):
        django_user_model.objects.create_user(username="jwt-user-3", password="jwt-pass-3")
        client = APIClient()

        login_res = client.post(
            "/api/v1/token/",
            {"username": "jwt-user-3", "password": "jwt-pass-3"},
            format="json",
        )
        assert login_res.status_code == 200

        refresh_token = login_res.cookies["refresh"].value
        refresh_res = client.post(
            "/api/v1/token/refresh/",
            {"refresh": refresh_token},
            format="json",
        )

        assert refresh_res.status_code == 200
        assert refresh_res.data["detail"] == "Token updated successfully."
        assert "access" in refresh_res.cookies

    def test_refresh_accepts_cookie_without_refresh_in_body(self, django_user_model):
        django_user_model.objects.create_user(username="jwt-user-cookie", password="jwt-pass-cookie")
        client = APIClient()

        login_res = client.post(
            "/api/v1/token/",
            {"username": "jwt-user-cookie", "password": "jwt-pass-cookie"},
            format="json",
        )
        assert login_res.status_code == 200

        refresh_res = client.post("/api/v1/token/refresh/", {}, format="json")

        assert refresh_res.status_code == 200
        assert refresh_res.data["detail"] == "Token updated successfully."
        assert "access" in refresh_res.cookies

    def test_refresh_rotates_token_and_invalidates_previous_one(self, django_user_model):
        django_user_model.objects.create_user(username="jwt-user-rotate", password="jwt-pass-rotate")
        client = APIClient()

        login_res = client.post(
            "/api/v1/token/",
            {"username": "jwt-user-rotate", "password": "jwt-pass-rotate"},
            format="json",
        )
        assert login_res.status_code == 200

        old_refresh = login_res.cookies["refresh"].value

        refresh_res = client.post(
            "/api/v1/token/refresh/",
            {"refresh": old_refresh},
            format="json",
        )

        assert refresh_res.status_code == 200
        assert "refresh" in refresh_res.cookies
        new_refresh = refresh_res.cookies["refresh"].value
        assert new_refresh != old_refresh

        reused_refresh_res = client.post(
            "/api/v1/token/refresh/",
            {"refresh": old_refresh},
            format="json",
        )

        assert reused_refresh_res.status_code == 401

    def test_logout_clears_cookies(self, django_user_model):
        django_user_model.objects.create_user(username="jwt-user-4", password="jwt-pass-4")
        client = APIClient()

        login_res = client.post(
            "/api/v1/token/",
            {"username": "jwt-user-4", "password": "jwt-pass-4"},
            format="json",
        )
        assert login_res.status_code == 200

        logout_res = client.post("/api/v1/logout/", {}, format="json")

        assert logout_res.status_code == 200
        assert logout_res.data["detail"] == "Logout successful."
        assert logout_res.cookies["access"].value == ""
        assert logout_res.cookies["refresh"].value == ""
