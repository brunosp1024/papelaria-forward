import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestJWTAuthentication:

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
