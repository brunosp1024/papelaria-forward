from decimal import Decimal

import pytest

from apps.product.tests.factories import ProductFactory
from apps.sale.models.sale_item import SaleItem
from apps.sale.tests.factories import SaleFactory


class TestSaleModel:

    def test_str_returns_invoice_number(self):
        sale = SaleFactory.build(invoice_number='INV-00099')
        assert str(sale) == 'NF INV-00099'

    @pytest.mark.django_db
    def test_total_value_sums_all_item_subtotals(self):
        sale = SaleFactory()
        p1 = ProductFactory(code='PROD-A', unit_value=Decimal('10.00'), commission_percentage=Decimal('5.00'))
        p2 = ProductFactory(code='PROD-B', unit_value=Decimal('20.00'), commission_percentage=Decimal('10.00'))
        SaleItem.objects.create(sale=sale, product=p1, quantity=2)  # 20
        SaleItem.objects.create(sale=sale, product=p2, quantity=1)  # 20

        assert sale.total_value == Decimal('40.00')

    @pytest.mark.django_db
    def test_total_commission_sums_all_item_commissions(self):
        sale = SaleFactory()
        p1 = ProductFactory(code='PROD-C', unit_value=Decimal('10.00'), commission_percentage=Decimal('10.00'))
        p2 = ProductFactory(code='PROD-D', unit_value=Decimal('20.00'), commission_percentage=Decimal('5.00'))
        SaleItem.objects.create(sale=sale, product=p1, quantity=2)  # 20 -> 2
        SaleItem.objects.create(sale=sale, product=p2, quantity=1)  # 20 -> 1

        assert sale.total_commission == Decimal('3.00')


@pytest.mark.django_db
class TestSaleItemModel:

    def test_str_contains_product_code_and_quantity(self):
        sale = SaleFactory()
        product = ProductFactory(code='PROD-STR', unit_value=Decimal('10.00'), commission_percentage=Decimal('5.00'))
        item = SaleItem.objects.create(sale=sale, product=product, quantity=3)

        assert str(item) == 'PROD-STR x3'

    def test_subtotal_multiplies_unit_value_by_quantity(self):
        sale = SaleFactory()
        product = ProductFactory(unit_value=Decimal('12.50'), commission_percentage=Decimal('5.00'))
        item = SaleItem.objects.create(sale=sale, product=product, quantity=4)

        assert item.subtotal == Decimal('50.00')
