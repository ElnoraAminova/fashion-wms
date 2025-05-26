from django.contrib import admin
from .models import WarehouseItem

@admin.register(WarehouseItem)
class WarehouseItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'stock', 'location')
    search_fields = ('product__name', 'location')
    list_filter = ('location',)
