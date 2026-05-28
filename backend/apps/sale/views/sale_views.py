from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from apps.core.authentication import CookieJWTAuthentication

from apps.sale.filters import SaleFilter

from apps.sale.models.sale import Sale
from apps.sale.serializers.sale_serializers import SaleReadSerializer, SaleWriteSerializer


class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    permission_resource = 'sales'
    serializer_class = SaleReadSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication, BasicAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['invoice_number']
    ordering_fields = ['invoice_number', 'datetime', 'created_at']
    filterset_class = SaleFilter
    serializer_classes = {
        'create': SaleWriteSerializer,
        'list': SaleReadSerializer,
        'retrieve': SaleReadSerializer,
        'update': SaleWriteSerializer,
        'partial_update': SaleWriteSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)