from django.shortcuts import render, redirect
from .models import WarehouseItem
from .forms import WarehouseItemForm

def warehouse_list(request):
    items = WarehouseItem.objects.select_related('product').all()
    return render(request, 'warehouse/list.html', {'items': items})


def warehouse_create(request):
    if request.method == 'POST':
        form = WarehouseItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('warehouse-list')
    else:
        form = WarehouseItemForm()
    
    return render(request, 'warehouse/create.html', {'form': form})
