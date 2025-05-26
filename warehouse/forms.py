from django import forms
from .models import WarehouseItem

class WarehouseItemForm(forms.ModelForm):
    class Meta:
        model = WarehouseItem
        fields = ['product', 'stock', 'location']
