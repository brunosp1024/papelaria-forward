import django_filters

from .models.sale import Sale


class SaleFilter(django_filters.FilterSet):
    invoice_number = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Sale
        fields = ['invoice_number', 'customer', 'seller']
