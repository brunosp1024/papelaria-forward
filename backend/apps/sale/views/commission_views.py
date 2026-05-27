from datetime import datetime, timedelta
from django.db.models import Count, Sum, Q, Value, DecimalField, F, ExpressionWrapper
from django.db.models.functions import Coalesce
from rest_framework.viewsets import ModelViewSet

from apps.sale.serializers.commission_serializers import CommissionConfigSerializer
from apps.sale.models.commission_config import CommissionConfig
from apps.seller.models import Seller


class CommissionConfigViewSet(ModelViewSet):
    queryset = CommissionConfig.objects.all().order_by("day_of_week")
    serializer_class = CommissionConfigSerializer

    def get_queryset(self):
        queryset = Seller.objects.all()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        sales_filter = Q()

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            sales_filter = Q(sales__datetime__gte=start_date, sales__datetime__lt=end_date)

        commission_expr = ExpressionWrapper(
            F('sales__items__quantity')
            * F('sales__items__product__unit_value')
            * F('sales__items__product__commission_percentage')
            / Value(100),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )

        queryset = queryset.annotate(
            sales_count=Count('sales', filter=sales_filter, distinct=True),
            commission_total=Coalesce(
                Sum(commission_expr, filter=sales_filter),
                Value(0),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ).order_by('code')

        if start_date and end_date:
            queryset = queryset.filter(sales_count__gt=0)

        return queryset
