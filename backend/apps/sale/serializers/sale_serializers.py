from rest_framework import serializers

from apps.sale.models.sale import Sale
from apps.customer.serializers import CustomerDetailSerializer as CustomerSerializer
from apps.seller.serializers import SellerDetailSerializer as SellerSerializer
from apps.sale.models.sale_item import SaleItem
from apps.sale.serializers.sale_item_serializers import SaleItemReadSerializer, SaleItemWriteSerializer


class SaleReadSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    seller = SellerSerializer(read_only=True)
    items = SaleItemReadSerializer(many=True, read_only=True)
    total_value = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_commission = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Sale
        fields = [
            "id", "invoice_number", "datetime",
            "customer", "seller", "items",
            "total_value", "total_commission", "created_at"
        ]


class SaleWriteSerializer(serializers.ModelSerializer):
    items = SaleItemWriteSerializer(many=True)

    class Meta:
        model = Sale
        fields = ["id", "datetime", "customer", "seller", "items"]

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("A venda deve ter ao menos um item.")
        return value

    def _current_user(self):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and getattr(user, 'is_authenticated', False):
            return user
        return None

    def create(self, validated_data):
        items_data = validated_data.pop("items", None)
        user = self._current_user()
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        sale = Sale.objects.create(**validated_data)
        if items_data is not None:
            for item in items_data:
                SaleItem.objects.create(sale=sale, **item)
        return sale

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_by = self._current_user()
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item in items_data:
                SaleItem.objects.create(sale=instance, **item)
        return instance