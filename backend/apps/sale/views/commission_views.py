from datetime import datetime, timedelta

from django.db.models import DecimalField, ExpressionWrapper, F, Q, Sum, Value, Count
from django.db.models.functions import Coalesce
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.sale.serializers.commission_serializers import (
    CommissionConfigSerializer,
    SellerCommissionSummarySerializer,
)
from apps.sale.models.commission_config import CommissionConfig
from apps.sale.models.sale import Sale
from apps.seller.models import Seller


class CommissionConfigViewSet(ModelViewSet):
    queryset = CommissionConfig.objects.all().order_by("day_of_week")
    serializer_class = CommissionConfigSerializer

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        print("Start date:", start_date, "End date:", end_date)

        sales_filter = Q()
        if start_date and end_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
            sales_filter = Q(datetime__gte=start, datetime__lt=end)

        sales_in_period = Sale.objects.filter(sales_filter)

        commission_expr = ExpressionWrapper(
            F("items__quantity")
            * F("items__product__unit_value")
            * F("items__product__commission_percentage")
            / Value(100),
            output_field=DecimalField(max_digits=10, decimal_places=2),
        )

        summary = (
            sales_in_period.values("seller__id", "seller__code", "seller__name")
            .annotate(
                total_sales=Count("id", distinct=True),
                total_commission=Coalesce(Sum(commission_expr), Value(0), output_field=DecimalField(max_digits=10, decimal_places=2)),
            )
            .order_by("seller__code")
        )

        seller_ids = [row["seller__id"] for row in summary]
        sellers = Seller.objects.in_bulk(seller_ids)

        payload = []
        for row in summary:
            seller = sellers.get(row["seller__id"])
            payload.append({
                "seller": seller,
                "total_sales": row["total_sales"],
                "total_commission": row["total_commission"],
            })

        serializer = SellerCommissionSummarySerializer(payload, many=True)
        return Response(serializer.data)
