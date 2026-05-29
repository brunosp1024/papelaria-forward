from django.contrib import admin
from .models import Seller


class SellerAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "phone", "email")
    list_display_links = ("name", "code")
    search_fields = ("name", "code", "phone", "email")
    list_per_page = 20


admin.site.register(Seller, SellerAdmin)
