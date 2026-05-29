from django.contrib import admin

from .models.sale import Sale
from .models.sale_item import SaleItem
from .models.commission_config import CommissionConfig


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "datetime", "customer", "seller")
    search_fields = ("invoice_number",)
    ordering = ("-datetime",)


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ("sale", "product", "quantity")
    search_fields = ("sale__invoice_number", "product__name")
    ordering = ("-sale__datetime",)


@admin.register(CommissionConfig)
class CommissionConfigAdmin(admin.ModelAdmin):
    list_display = ("day_of_week", "min_percentage", "max_percentage")
    search_fields = ("day_of_week",)
    ordering = ("day_of_week",)
