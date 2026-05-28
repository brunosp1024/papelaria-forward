from datetime import datetime, timedelta

from django.db.models import DecimalField, ExpressionWrapper, F, Q, Sum, Value
from django.db.models.functions import Coalesce
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.sale.serializers.commission_serializers import (
    CommissionConfigSerializer,
    SellerCommissionSummarySerializer,
)
from apps.sale.models.commission_config import CommissionConfig
from apps.seller.models import Seller


class CommissionConfigViewSet(ModelViewSet):
    queryset = CommissionConfig.objects.all().order_by("day_of_week")
    serializer_class = CommissionConfigSerializer

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        queryset = Seller.objects.all().order_by("code")

        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        sales_filter = Q()

        if start_date and end_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
            sales_filter = Q(sales__datetime__gte=start, sales__datetime__lt=end)

        commission_expr = ExpressionWrapper(
            F("sales__items__quantity")
            * F("sales__items__product__unit_value")
            * F("sales__items__product__commission_percentage")
            / Value(100),
            output_field=DecimalField(max_digits=10, decimal_places=2),
        )

        queryset = queryset.annotate(
            total_commission=Coalesce(
                Sum(commission_expr, filter=sales_filter),
                Value(0),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )

        payload = [
            {"seller": seller, "total_commission": seller.total_commission}
            for seller in queryset
        ]
        serializer = SellerCommissionSummarySerializer(payload, many=True)
        return Response(serializer.data)
