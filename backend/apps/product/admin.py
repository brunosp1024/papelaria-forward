from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "unit_value", "commission_percentage")
    list_display_links = ("code", "description")
    search_fields = ("code", "description")
    list_per_page = 20


admin.site.register(Product, ProductAdmin)
