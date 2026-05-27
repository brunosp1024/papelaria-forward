from datetime import datetime, timezone
from decimal import Decimal

import pytest

from apps.customer.tests.factories import CustomerFactory
from apps.product.tests.factories import ProductFactory
from apps.sale.models.commission_config import CommissionConfig
from apps.sale.models.sale_item import SaleItem
from apps.sale.services.commission_summary import get_commission_summary
from apps.sale.tests.factories import SaleFactory
from apps.seller.tests.factories import SellerFactory


@pytest.mark.django_db
class TestCommissionSummaryService:

    def test_groups_totals_by_seller_for_period(self):
        period_start = datetime(2026, 5, 1, tzinfo=timezone.utc).date()
        period_end = datetime(2026, 5, 31, tzinfo=timezone.utc).date()
        sale_date = datetime(2026, 5, 20, 12, 0, tzinfo=timezone.utc)  # Wednesday
        outside_date = datetime(2026, 6, 2, 12, 0, tzinfo=timezone.utc)

        CommissionConfig.objects.create(
            day_of_week=2,
            min_percentage=Decimal('3.00'),
            max_percentage=Decimal('6.00'),
        )

        seller_a = SellerFactory(name='Alice Seller')
        seller_b = SellerFactory(name='Bruno Seller')
        customer = CustomerFactory()

        sale_a = SaleFactory(
            seller=seller_a,
            customer=customer,
            datetime=sale_date,
            invoice_number='INV-SVC-001',
        )
        product_a1 = ProductFactory(unit_value=Decimal('100.00'), commission_percentage=Decimal('10.00'))
        product_a2 = ProductFactory(unit_value=Decimal('50.00'), commission_percentage=Decimal('1.00'))
        SaleItem.objects.create(sale=sale_a, product=product_a1, quantity=1)
        SaleItem.objects.create(sale=sale_a, product=product_a2, quantity=2)

        sale_b = SaleFactory(
            seller=seller_b,
            customer=customer,
            datetime=sale_date,
            invoice_number='INV-SVC-002',
        )
        product_b1 = ProductFactory(unit_value=Decimal('100.00'), commission_percentage=Decimal('4.00'))
        SaleItem.objects.create(sale=sale_b, product=product_b1, quantity=1)

        sale_outside = SaleFactory(
            seller=seller_a,
            customer=customer,
            datetime=outside_date,
            invoice_number='INV-SVC-003',
        )
        product_outside = ProductFactory(unit_value=Decimal('100.00'), commission_percentage=Decimal('10.00'))
        SaleItem.objects.create(sale=sale_outside, product=product_outside, quantity=1)

        summary = get_commission_summary(period_start, period_end)

        assert len(summary) == 2
        assert summary[0]['seller'] == seller_a
        assert summary[0]['total_commission'] == Decimal('9.00')
        assert summary[1]['seller'] == seller_b
        assert summary[1]['total_commission'] == Decimal('4.00')
