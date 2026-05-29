from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from apps.core.authentication import CookieJWTAuthentication

from apps.seller.filters import SellerFilter

from .models import Seller
from .serializers import (
    SellerCreateUpdateSerializer,
    SellerListSerializer,
    SellerDetailSerializer,
)


class SellerViewSet(ModelViewSet):
    queryset = Seller.objects.all()
    permission_resource = "sellers"
    serializer_class = SellerListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [
        CookieJWTAuthentication,
        BasicAuthentication,
        SessionAuthentication,
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name", "email"]
    ordering_fields = ["name", "created_at"]
    filterset_class = SellerFilter
    serializer_classes = {
        "create": SellerCreateUpdateSerializer,
        "list": SellerListSerializer,
        "retrieve": SellerDetailSerializer,
        "update": SellerCreateUpdateSerializer,
        "partial_update": SellerCreateUpdateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)
