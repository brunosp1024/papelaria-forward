from collections import defaultdict
from decimal import Decimal

from apps.sale.models.commission_config import CommissionConfig
from apps.sale.models.sale import Sale


def get_commission_summary(start_date, end_date):
    sales = (
        Sale.objects.filter(datetime__date__range=(start_date, end_date))
        .select_related('seller')
        .prefetch_related('items__product')
    )
    configs = {config.day_of_week: config for config in CommissionConfig.objects.all()}
    seller_totals = defaultdict(lambda: Decimal('0.00'))
    sellers = {}

    for sale in sales:
        sellers[sale.seller_id] = sale.seller
        config = configs.get(sale.datetime.weekday())

        for item in sale.items.all():
            percentage = item.product.commission_percentage
            if config is not None:
                percentage = max(config.min_percentage, min(percentage, config.max_percentage))
            seller_totals[sale.seller_id] += (percentage / Decimal('100')) * item.subtotal

    payload = [
        {
            'seller': sellers[seller_id],
            'total_commission': total.quantize(Decimal('0.01')),
        }
        for seller_id, total in seller_totals.items()
    ]
    payload.sort(key=lambda item: item['seller'].name)
    return payload