from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Products
    path('products/', views.product_list, name='product-list'),
    path('products/new/', views.product_create, name='product-create'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/<int:pk>/update/', views.product_update, name='product-update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product-delete'),

    # Categories
    path('categories/', views.category_list, name='category-list'),
    path('categories/new/', views.category_create, name='category-create'),
    path('categories/<int:pk>/update/', views.category_update, name='category-update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category-delete'),

    # Customers
    path('customers/', views.customer_list, name='customer-list'),
    path('customers/new/', views.customer_create, name='customer-create'),
    path('customers/<int:pk>/', views.customer_detail, name='customer-detail'),
    path('customers/<int:pk>/update/', views.customer_update, name='customer-update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer-delete'),

    # Orders
    path('orders/', views.order_list, name='order-list'),
    path('orders/new/', views.order_create, name='order-create'),
    path('orders/<int:pk>/', views.order_detail, name='order-detail'),
    path('orders/<int:pk>/update/', views.order_update, name='order-update'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order-delete'),
]