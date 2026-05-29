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

        sales_filter = Q()
        if start_date and end_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
            sales_filter = Q(datetime__gte=start, datetime__lt=end)

        sales_in_period = Sale.objects.filter(sales_filter).prefetch_related("items__product", "seller")

        seller_data = {}

        for sale in sales_in_period:
            seller = sale.seller
            if seller.id not in seller_data:
                seller_data[seller.id] = {
                    "seller": seller,
                    "total_sales": 0,
                    "total_commission": 0,
                }
            seller_data[seller.id]["total_sales"] += 1
            for item in sale.items.all():
                seller_data[seller.id]["total_commission"] += float(item.commission_value)

        payload = list(seller_data.values())
        serializer = SellerCommissionSummarySerializer(payload, many=True)
        return Response(serializer.data)
