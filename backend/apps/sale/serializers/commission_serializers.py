from rest_framework import serializers

from apps.sale.models.commission_config import CommissionConfig
from apps.seller.serializers import SellerListSerializer


class CommissionConfigSerializer(serializers.ModelSerializer):
    day_of_week_display = serializers.CharField(
        source="get_day_of_week_display", read_only=True
    )

    class Meta:
        model = CommissionConfig
        fields = [
            "id",
            "day_of_week",
            "day_of_week_display",
            "min_percentage",
            "max_percentage",
        ]

    def validate(self, data):
        min_percentage = data.get("min_percentage")
        max_percentage = data.get("max_percentage")

        if self.instance is not None:
            if min_percentage is None:
                min_percentage = self.instance.min_percentage
            if max_percentage is None:
                max_percentage = self.instance.max_percentage

        if (
            min_percentage is not None
            and max_percentage is not None
            and min_percentage > max_percentage
        ):
            raise serializers.ValidationError(
                "O percentual mínimo não pode ser maior que o máximo."
            )
        return data


class SellerCommissionSummarySerializer(serializers.Serializer):
    seller = SellerListSerializer(read_only=True)
    total_sales = serializers.IntegerField(read_only=True)
    total_commission = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
