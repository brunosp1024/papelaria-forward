from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from apps.core.authentication import CookieJWTAuthentication

from apps.customer.filters import CustomerFilter
from .models import Customer
from .serializers import CustomerCreateUpdateSerializer, CustomerListSerializer, CustomerDetailSerializer
from rest_framework.permissions import IsAuthenticated


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    permission_resource = 'customers'
    serializer_class = CustomerListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication, BasicAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'created_at']
    filterset_class = CustomerFilter
    serializer_classes = {
        'create': CustomerCreateUpdateSerializer,
        'list': CustomerListSerializer,
        'retrieve': CustomerDetailSerializer,
        'update': CustomerCreateUpdateSerializer,
        'partial_update': CustomerCreateUpdateSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
