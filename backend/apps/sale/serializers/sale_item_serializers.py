from rest_framework import serializers

from apps.sale.models.sale_item import SaleItem
from apps.product.serializers import ProductDetailSerializer as ProductSerializer


class SaleItemReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    commission_value = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = SaleItem
        fields = ["id", "product", "quantity", "subtotal", "commission_value"]


class SaleItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ["product", "quantity"]
