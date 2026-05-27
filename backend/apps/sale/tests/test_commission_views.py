from datetime import datetime, timezone
from decimal import Decimal

import pytest

from apps.customer.tests.factories import CustomerFactory
from apps.product.tests.factories import ProductFactory
from apps.sale.models.commission_config import CommissionConfig
from apps.sale.models.sale_item import SaleItem
from apps.sale.tests.factories import SaleFactory
from apps.seller.tests.factories import SellerFactory


SUMMARY_URL = '/api/v1/commission-configs/commission-summary/'


@pytest.mark.django_db
class TestCommissionSummaryAction:

    def test_requires_start_date(self, admin_client):
        res = admin_client.get(SUMMARY_URL)

        assert res.status_code == 400
        assert 'start_date' in res.data

    def test_requires_end_date(self, admin_client):
        res = admin_client.get(SUMMARY_URL, {'start_date': '2026-05-01'})

        assert res.status_code == 400
        assert 'end_date' in res.data

    def test_requires_end_date_after_start_date(self, admin_client):
        res = admin_client.get(
            SUMMARY_URL,
            {'start_date': '2026-05-20', 'end_date': '2026-05-01'},
        )

        assert res.status_code == 400
        assert 'end_date' in res.data

    def test_returns_summary_grouped_by_seller(self, admin_client):
        sale_date = datetime(2026, 5, 20, 12, 0, tzinfo=timezone.utc)  # Wednesday

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
            invoice_number='INV-VIEW-001',
        )
        product_a = ProductFactory(unit_value=Decimal('100.00'), commission_percentage=Decimal('10.00'))
        SaleItem.objects.create(sale=sale_a, product=product_a, quantity=1)

        sale_b = SaleFactory(
            seller=seller_b,
            customer=customer,
            datetime=sale_date,
            invoice_number='INV-VIEW-002',
        )
        product_b = ProductFactory(unit_value=Decimal('100.00'), commission_percentage=Decimal('4.00'))
        SaleItem.objects.create(sale=sale_b, product=product_b, quantity=1)

        res = admin_client.get(
            SUMMARY_URL,
            {'start_date': '2026-05-01', 'end_date': '2026-05-31'},
        )

        assert res.status_code == 200
        assert len(res.data) == 2

        by_seller_id = {item['seller']['id']: item for item in res.data}
        assert by_seller_id[str(seller_a.pk)]['total_commission'] == '6.00'
        assert by_seller_id[str(seller_b.pk)]['total_commission'] == '4.00'
