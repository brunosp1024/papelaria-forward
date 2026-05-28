from decimal import Decimal

import pytest

from apps.customer.tests.factories import CustomerFactory
from apps.product.tests.factories import ProductFactory
from apps.sale.models.sale_item import SaleItem
from apps.sale.models.sale import Sale
from apps.sale.tests.factories import SaleFactory
from apps.seller.tests.factories import SellerFactory


class TestSaleModel:
    @pytest.mark.django_db
    def test_invoice_number_generated_on_create(self):
        customer = CustomerFactory()
        seller = SellerFactory()
        sale = Sale.objects.create(datetime='2024-01-01T00:00:00Z', customer=customer, seller=seller)
        assert sale.invoice_number is not None
        assert sale.invoice_number.isdigit()
        assert len(sale.invoice_number) == 9

    @pytest.mark.django_db
    def test_invoice_number_not_changed_on_update(self):
        customer = CustomerFactory()
        seller = SellerFactory()
        sale = Sale.objects.create(datetime='2024-01-01T00:00:00Z', customer=customer, seller=seller)
        original_invoice = sale.invoice_number
        sale.datetime = '2024-01-02T00:00:00Z'
        sale.save()
        sale.refresh_from_db()
        assert sale.invoice_number == original_invoice

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
