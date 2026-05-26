import django_filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['code', 'description']
