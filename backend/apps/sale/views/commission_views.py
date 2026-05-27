from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from apps.sale.serializers.commission_serializers import CommissionConfigSerializer, SellerCommissionSummarySerializer
from apps.sale.models.commission_config import CommissionConfig
from apps.sale.services.commission_summary import get_commission_summary
from utils.date_parsers import parse_date_param


class CommissionConfigViewSet(ModelViewSet):
    queryset = CommissionConfig.objects.all().order_by("day_of_week")
    serializer_class = CommissionConfigSerializer

    def create(self, request, *args, **kwargs):
        day = request.data.get("day_of_week")
        instance = CommissionConfig.objects.filter(day_of_week=day).first()

        if instance:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='commission-summary')
    def commission_summary(self, request):
        start_date = parse_date_param(request.query_params.get('start_date'), 'start_date')
        end_date = parse_date_param(request.query_params.get('end_date'), 'end_date')

        if start_date > end_date:
            raise ValidationError({'end_date': 'A data final deve ser maior ou igual à data inicial.'})

        serializer = SellerCommissionSummarySerializer(
            get_commission_summary(start_date, end_date),
            many=True,
        )
        return Response(serializer.data)
