from django.contrib import admin
from django.urls import include, path
from apps.core.views import (
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    LogoutView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.customer.urls")),
    path("api/v1/", include("apps.seller.urls")),
    path("api/v1/", include("apps.product.urls")),
    path("api/v1/", include("apps.sale.urls")),
    # JWT endpoints
    path(
        "api/v1/token/", CookieTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/v1/token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/v1/logout/", LogoutView.as_view(), name="logout"),
]
