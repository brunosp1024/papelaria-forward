from datetime import datetime, timezone
from decimal import Decimal

import pytest
from rest_framework.test import APIRequestFactory

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

    def test_get_queryset_returns_all_sellers_with_annotations_without_period(self):
        customer = CustomerFactory()
        seller_a = SellerFactory(code='S00001', name='Alice Seller')
        seller_b = SellerFactory(code='S00002', name='Bruno Seller')

        sale = SaleFactory(
            seller=seller_a,
            customer=customer,
            datetime=datetime(2026, 5, 20, 12, 0, tzinfo=timezone.utc),
            invoice_number='INV-QS-001',
        )
        product = ProductFactory(unit_value=Decimal('100.00'), commission_percentage=Decimal('10.00'))
        SaleItem.objects.create(sale=sale, product=product, quantity=2)

        sellers = list(build_view().get_queryset())

        assert [seller.code for seller in sellers] == ['S00001', 'S00002']

        seller_a_row = next(item for item in sellers if item.pk == seller_a.pk)
        seller_b_row = next(item for item in sellers if item.pk == seller_b.pk)

        assert seller_a_row.sales_count == 1
        assert seller_a_row.commission_total == Decimal('20.00')
        assert seller_b_row.sales_count == 0
        assert seller_b_row.commission_total == Decimal('0.00')

    def test_get_queryset_filters_to_sellers_with_sales_in_period(self):
        customer = CustomerFactory()
        seller_in_period = SellerFactory(code='S00003', name='In Period')
        seller_outside_period = SellerFactory(code='S00004', name='Outside Period')

        sale_in_period = SaleFactory(
            seller=seller_in_period,
            customer=customer,
            datetime=datetime(2026, 5, 20, 12, 0, tzinfo=timezone.utc),
            invoice_number='INV-QS-002',
        )
        product_in_period = ProductFactory(unit_value=Decimal('50.00'), commission_percentage=Decimal('4.00'))
        SaleItem.objects.create(sale=sale_in_period, product=product_in_period, quantity=1)

        sale_outside_period = SaleFactory(
            seller=seller_outside_period,
            customer=customer,
            datetime=datetime(2026, 6, 5, 12, 0, tzinfo=timezone.utc),
            invoice_number='INV-QS-003',
        )
        product_outside_period = ProductFactory(unit_value=Decimal('80.00'), commission_percentage=Decimal('5.00'))
        SaleItem.objects.create(sale=sale_outside_period, product=product_outside_period, quantity=1)

        sellers = list(
            build_view({'start_date': '2026-05-01', 'end_date': '2026-05-31'}).get_queryset()
        )

        assert [seller.pk for seller in sellers] == [seller_in_period.pk]
        assert sellers[0].sales_count == 1
        assert sellers[0].commission_total == Decimal('2.00')
