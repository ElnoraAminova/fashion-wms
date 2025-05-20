from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, F, DecimalField
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta

from .models import Category, Product, Customer, Order, OrderItem
from .forms import (
    CategoryForm, ProductForm, CustomerForm,
    OrderForm, OrderItemFormSet
)


# Dashboard views
@login_required
def dashboard(request):
    """Bosh sahifa - Dashboard"""
    # So'nggi 30 kun uchun statistika
    thirty_days_ago = timezone.now() - timedelta(days=30)

    # Asosiy statistika
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()

    # So'nggi 30 kundagi buyurtmalar
    recent_orders = Order.objects.filter(created_at__gte=thirty_days_ago)

    # Kunlik daromad (so'nggi 30 kun)
    daily_revenue = recent_orders.annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        revenue=Sum(F('items__price') * F('items__quantity'), output_field=DecimalField())
    ).order_by('date')

    # Eng ko'p sotilgan mahsulotlar
    top_products = OrderItem.objects.values(
        'product__name'
    ).annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')[:5]

    # Buyurtmalar statusi
    order_status = Order.objects.values('status').annotate(count=Count('id'))

    # So'nggi buyurtmalar
    latest_orders = Order.objects.select_related('customer').order_by('-created_at')[:5]

    # Kam qolgan mahsulotlar (stock < 10)
    low_stock_products = Product.objects.filter(stock__lt=10).order_by('stock')[:5]

    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'daily_revenue': daily_revenue,
        'top_products': top_products,
        'order_status': order_status,
        'latest_orders': latest_orders,
        'low_stock_products': low_stock_products,
    }

    return render(request, 'dashboard/dashboard.html', context)


# Product views
@login_required
def product_list(request):
    """Mahsulotlar ro'yxati"""
    products = Product.objects.select_related('category').all()
    return render(request, 'products/product_list.html', {'products': products})


@login_required
def product_detail(request, pk):
    """Mahsulot tafsilotlari"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
def product_create(request):
    """Yangi mahsulot qo'shish"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mahsulot muvaffaqiyatli qo\'shildi!')
            return redirect('product-list')
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {'form': form, 'title': 'Yangi mahsulot qo\'shish'})


@login_required
def product_update(request, pk):
    """Mahsulotni yangilash"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mahsulot muvaffaqiyatli yangilandi!')
            return redirect('product-detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Mahsulotni yangilash',
        'product': product
    })


@login_required
def product_delete(request, pk):
    """Mahsulotni o'chirish"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Mahsulot muvaffaqiyatli o\'chirildi!')
        return redirect('product-list')

    return render(request, 'products/product_confirm_delete.html', {'product': product})


# Customer views
@login_required
def customer_list(request):
    """Mijozlar ro'yxati"""
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})


@login_required
def customer_detail(request, pk):
    """Mijoz tafsilotlari"""
    customer = get_object_or_404(Customer, pk=pk)
    # Mijozning buyurtmalari
    orders = customer.orders.all().order_by('-created_at')

    return render(request, 'customers/customer_detail.html', {
        'customer': customer,
        'orders': orders
    })


@login_required
def customer_create(request):
    """Yangi mijoz qo'shish"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mijoz muvaffaqiyatli qo\'shildi!')
            return redirect('customer-list')
    else:
        form = CustomerForm()

    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Yangi mijoz qo\'shish'})


@login_required
def customer_update(request, pk):
    """Mijozni yangilash"""
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mijoz muvaffaqiyatli yangilandi!')
            return redirect('customer-detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/customer_form.html', {
        'form': form,
        'title': 'Mijozni yangilash',
        'customer': customer
    })


@login_required
def customer_delete(request, pk):
    """Mijozni o'chirish"""
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Mijoz muvaffaqiyatli o\'chirildi!')
        return redirect('customer-list')

    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})


# Order views
@login_required
def order_list(request):
    """Buyurtmalar ro'yxati"""
    orders = Order.objects.select_related('customer').all().order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    """Buyurtma tafsilotlari"""
    order = get_object_or_404(Order, pk=pk)
    # Buyurtma elementlari
    items = order.items.select_related('product').all()

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items,
        'total': order.get_total_price()
    })


@login_required
def order_create(request):
    """Yangi buyurtma yaratish"""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()

            formset = OrderItemFormSet(request.POST, instance=order)
            if formset.is_valid():
                # Har bir element uchun narxni mahsulotdan olish
                for form in formset:
                    if form.cleaned_data.get('product'):
                        item = form.save(commit=False)
                        item.price = item.product.price
                        item.save()

                        # Mahsulot sonini kamaytirish
                        product = item.product
                        product.stock -= item.quantity
                        product.save()

                messages.success(request, 'Buyurtma muvaffaqiyatli yaratildi!')
                return redirect('order-detail', pk=order.pk)
    else:
        form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, 'orders/order_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Yangi buyurtma yaratish'
    })


@login_required
def order_update(request, pk):
    """Buyurtmani yangilash"""
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()

            formset = OrderItemFormSet(request.POST, instance=order)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Buyurtma muvaffaqiyatli yangilandi!')
                return redirect('order-detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)

    return render(request, 'orders/order_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Buyurtmani yangilash',
        'order': order
    })


@login_required
def order_delete(request, pk):
    """Buyurtmani o'chirish"""
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        # Mahsulot sonini qaytarish
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()

        order.delete()
        messages.success(request, 'Buyurtma muvaffaqiyatli o\'chirildi!')
        return redirect('order-list')

    return render(request, 'orders/order_confirm_delete.html', {'order': order})


# Category views
@login_required
def category_list(request):
    """Kategoriyalar ro'yxati"""
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    """Yangi kategoriya qo'shish"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategoriya muvaffaqiyatli qo\'shildi!')
            return redirect('category-list')
    else:
        form = CategoryForm()

    return render(request, 'products/category_form.html',
                  {'form': form, 'title': 'Yangi kategoriya qo\'shish'})


@login_required
def category_update(request, pk):
    """Kategoriyani yangilash"""
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategoriya muvaffaqiyatli yangilandi!')
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'products/category_form.html', {
        'form': form,
        'title': 'Kategoriyani yangilash',
        'category': category
    })


@login_required
def category_delete(request, pk):
    """Kategoriyani o'chirish"""
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Kategoriya muvaffaqiyatli o\'chirildi!')
        return redirect('category-list')

    return render(request, 'products/category_confirm_delete.html', {'category': category})