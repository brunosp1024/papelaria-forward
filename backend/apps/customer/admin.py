from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    list_display_links = ('name', 'phone')
    search_fields = ('name', 'phone')
    list_per_page = 20

admin.site.register(Customer, CustomerAdmin)