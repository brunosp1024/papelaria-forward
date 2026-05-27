import pytest
from decimal import Decimal
from datetime import datetime, timezone
from django.core.exceptions import ValidationError
from apps.sale.models.commission_config import CommissionConfig
from apps.product.tests.factories import ProductFactory
from apps.sale.tests.factories import SaleFactory
from apps.sale.models.sale_item import SaleItem


@pytest.mark.django_db
class TestCommissionCalculation:

    SALE_DATETIME = datetime(2026, 5, 27, 12, 0, tzinfo=timezone.utc)  # Wednesday (2)
    SALE_WEEKDAY = 2

    def test_commission_without_config(self):
        product = ProductFactory(unit_value=Decimal("100"), commission_percentage=Decimal("5"))
        sale = SaleFactory()
        item = SaleItem.objects.create(sale=sale, product=product, quantity=2)
        assert item.commission_value == Decimal("10.00")  # 5% of 200

    def test_commission_capped_by_max(self):
        CommissionConfig.objects.create(
            day_of_week=self.SALE_WEEKDAY,
            min_percentage=Decimal("0"),
            max_percentage=Decimal("3")
        )
        product = ProductFactory(unit_value=Decimal("100"), commission_percentage=Decimal("10"))
        sale = SaleFactory(datetime=self.SALE_DATETIME)
        item = SaleItem.objects.create(sale=sale, product=product, quantity=1)
        assert item.commission_value == Decimal("3.00")  # capped by max

    def test_commission_floored_by_min(self):
        CommissionConfig.objects.create(
            day_of_week=self.SALE_WEEKDAY,
            min_percentage=Decimal("5"),
            max_percentage=Decimal("10")
        )
        product = ProductFactory(unit_value=Decimal("100"), commission_percentage=Decimal("2"))
        sale = SaleFactory(datetime=self.SALE_DATETIME)
        item = SaleItem.objects.create(sale=sale, product=product, quantity=1)
        assert item.commission_value == Decimal("5.00")  # floored by min


@pytest.mark.django_db
class TestCommissionConfigModel:

    def test_clean_raises_when_min_greater_than_max(self):
        config = CommissionConfig(
            day_of_week=1,
            min_percentage=Decimal("6.00"),
            max_percentage=Decimal("5.00"),
        )

        with pytest.raises(ValidationError):
            config.clean()

    def test_day_of_week_must_be_unique(self):
        CommissionConfig.objects.create(
            day_of_week=2,
            min_percentage=Decimal("1.00"),
            max_percentage=Decimal("5.00"),
        )
        duplicate = CommissionConfig(
            day_of_week=2,
            min_percentage=Decimal("1.00"),
            max_percentage=Decimal("4.00"),
        )

        with pytest.raises(ValidationError):
            duplicate.validate_unique()

    def test_str_contains_weekday_and_ranges(self):
        config = CommissionConfig.objects.create(
            day_of_week=2,
            min_percentage=Decimal("1.00"),
            max_percentage=Decimal("5.00"),
        )

        assert str(config) == "Quarta-feira (1.00% - 5.00%)"
