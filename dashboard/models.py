from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Category(models.Model):
    """Mahsulot kategoriyalari"""
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


class Product(models.Model):
    """Mahsulotlar"""
    name = models.CharField(max_length=200, verbose_name="Mahsulot nomi")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Kategoriya")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    stock = models.PositiveIntegerField(default=0, verbose_name="Soni")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Rasm")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']


class Customer(models.Model):
    """Mijozlar"""
    first_name = models.CharField(max_length=100, verbose_name="Ismi")
    last_name = models.CharField(max_length=100, verbose_name="Familiyasi")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    address = models.TextField(verbose_name="Manzil")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('customer-detail', kwargs={'pk': self.pk})

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"
        ordering = ['-created_at']


class Order(models.Model):
    """Buyurtmalar"""
    STATUS_CHOICES = (
        ('new', 'Yangi'),
        ('paid', 'To\'langan'),
        ('delivered', 'Yetkazilgan'),
        ('cancelled', 'Bekor qilingan'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders", verbose_name="Mijoz")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_orders",
                                   verbose_name="Yaratuvchi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    note = models.TextField(blank=True, null=True, verbose_name="Izoh")

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.customer}"

    def get_absolute_url(self):
        return reverse('order-detail', kwargs={'pk': self.pk})

    def get_total_price(self):
        """Buyurtmaning umumiy narxini hisoblash"""
        return sum(item.get_cost() for item in self.items.all())

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']


class OrderItem(models.Model):
    """Buyurtma elementlari"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Buyurtma")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items", verbose_name="Mahsulot")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miqdori")

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        """Elementning umumiy narxini hisoblash"""
        return self.price * self.quantity

    class Meta:
        verbose_name = "Buyurtma elementi"
        verbose_name_plural = "Buyurtma elementlari"