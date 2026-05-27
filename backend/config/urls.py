from django.contrib import admin
from django.urls import include, path
from apps.core.views import CookieTokenObtainPairView, CookieTokenRefreshView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.customer.urls')),
    path('api/', include('apps.seller.urls')),
    path('api/', include('apps.product.urls')),
    path('api/', include('apps.sale.urls')),

    # JWT endpoints
    path('api/token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]
