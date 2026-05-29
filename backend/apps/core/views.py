from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class CookieTokenRefreshView(TokenRefreshView):
    """View to refresh JWT tokens using cookies."""

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request, *args, **kwargs):
        if "refresh" not in request.data:
            refresh_cookie = request.COOKIES.get("refresh")
            if refresh_cookie:
                payload = (
                    request.data.copy()
                    if hasattr(request.data, "copy")
                    else dict(request.data)
                )
                payload["refresh"] = refresh_cookie
                request._full_data = payload
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            access = response.data.get("access")
            refresh = response.data.get("refresh")
            # Update the access cookie
            response.set_cookie(
                key="access",
                value=access,
                httponly=True,
                samesite="Lax",
                max_age=60 * 60,  # 1 hour
                path="/",
            )
            if refresh:
                response.set_cookie(
                    key="refresh",
                    value=refresh,
                    httponly=True,
                    samesite="Lax",
                    max_age=60 * 60 * 24 * 3,  # 3 days
                    path="/",
                )
            response.data = {"detail": "Token updated successfully."}
        return response


class CookieTokenObtainPairView(TokenObtainPairView):
    """View to obtain JWT tokens and set them in cookies."""

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            access = response.data.get("access")
            refresh = response.data.get("refresh")
            response.set_cookie(
                key="access",
                value=access,
                httponly=True,
                samesite="Lax",
                max_age=60 * 60,  # 1 hour
                path="/",
            )
            response.set_cookie(
                key="refresh",
                value=refresh,
                httponly=True,
                samesite="Lax",
                max_age=60 * 60 * 24 * 3,  # 3 days
                path="/",
            )
            response.data = {"detail": "Login successful."}
        return response


class LogoutView(APIView):
    """View to handle user logout by deleting JWT cookies."""

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        response = Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        response.delete_cookie("access", path="/")
        response.delete_cookie("refresh", path="/")
        return response
