from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.product.filters import ProductFilter

from .models import Product
from .serializers import ProductCreateUpdateSerializer, ProductListSerializer, ProductDetailSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_resource = 'products'
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['code', 'description']
    ordering_fields = ['code', 'created_at']
    filterset_class = ProductFilter
    serializer_classes = {
        'create': ProductCreateUpdateSerializer,
        'list': ProductListSerializer,
        'retrieve': ProductDetailSerializer,
        'update': ProductCreateUpdateSerializer,
        'partial_update': ProductCreateUpdateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
