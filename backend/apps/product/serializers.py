

from rest_framework import serializers

from apps.product.models import Product


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'code',
            'description',
            'unit_value',
            'commission_percentage',
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
        ]
