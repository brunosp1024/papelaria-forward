from django.contrib import admin

from .models.sale import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'datetime', 'customer', 'seller')
    search_fields = ('invoice_number',)
    ordering = ('-datetime',)
