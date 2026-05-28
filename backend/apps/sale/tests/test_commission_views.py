from datetime import datetime, timezone
from decimal import Decimal

import pytest
from rest_framework.test import APIRequestFactory

from apps.sale.models.commission_config import CommissionConfig
from apps.customer.tests.factories import CustomerFactory
from apps.product.tests.factories import ProductFactory
from apps.sale.models.sale_item import SaleItem
from apps.sale.tests.factories import SaleFactory
from apps.sale.views.commission_views import CommissionConfigViewSet
from apps.seller.tests.factories import SellerFactory


def build_view(params=None):
    factory = APIRequestFactory()
    request = factory.get('/api/v1/commissions/', data=params or {})
    view = CommissionConfigViewSet()
    view.request = request
    return view


@pytest.mark.django_db
class TestCommissionConfigGetQueryset:
    def test_get_queryset_returns_commission_configs_ordered_by_day_of_week(self):
        config_wed = CommissionConfig.objects.create(
            day_of_week=2,
            min_percentage='2.50',
            max_percentage='6.00',
        )
        config_mon = CommissionConfig.objects.create(
            day_of_week=0,
            min_percentage='1.50',
            max_percentage='5.00',
        )

        configs = list(build_view().get_queryset())

        assert [item.pk for item in configs] == [config_mon.pk, config_wed.pk]

    def test_summary_returns_total_commission_grouped_by_seller(self):
        customer = CustomerFactory()
        seller = SellerFactory(code='S00001', name='Alice Seller')

        sale = SaleFactory(
            seller=seller,
            customer=customer,
            datetime=datetime(2026, 5, 20, 12, 0, tzinfo=timezone.utc),
            invoice_number='INV-SUMMARY-001',
        )
        product = ProductFactory(unit_value=Decimal('100.00'), commission_percentage=Decimal('10.00'))
        SaleItem.objects.create(sale=sale, product=product, quantity=2)

        factory = APIRequestFactory()
        request = factory.get(
            '/api/v1/commissions/summary/',
            data={'start_date': '2026-05-01', 'end_date': '2026-05-31'},
        )
        response = CommissionConfigViewSet.as_view({'get': 'summary'})(request)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['seller']['id'] == str(seller.id)
        assert response.data[0]['total_commission'] == '20.00'
