from rest_framework.routers import DefaultRouter

from .views import CommissionConfigViewSet, SaleViewSet


class OptionalSlashRouter(DefaultRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()
router.register(r'sales', SaleViewSet)
router.register(r'commission-configs', CommissionConfigViewSet)

urlpatterns = router.urls
