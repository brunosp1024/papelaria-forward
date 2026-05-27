from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from apps.sale.serializers.commission_serializers import CommissionConfigSerializer
from apps.sale.models.commission_config import CommissionConfig


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
