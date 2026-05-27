

from rest_framework import serializers

from apps.product.models import Product
from apps.core.serializers.audit_serializer_mixin import AuditSerializerMixin


class ProductCreateUpdateSerializer(AuditSerializerMixin):
    class Meta:
        model = Product
        fields = [
            'id',
            'code',
            'description',
            'unit_value',
            'commission_percentage'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'code',
            'description',
            'unit_value',
            'commission_percentage',
            'created_at',
            'updated_at',
            "created_by",
            "updated_by"
        ]


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'code',
            'description',
            'unit_value',
            'commission_percentage',
            'created_at',
            'updated_at',
            "created_by",
            "updated_by"
        ]
