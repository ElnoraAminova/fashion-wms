from django.db import models
from dashboard.models import Product

class WarehouseItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Mahsulot")
    stock = models.PositiveIntegerField(verbose_name="Zaxira soni")
    location = models.CharField(max_length=100, verbose_name="Joylashuvi")

    def __str__(self):
        return f"{self.product.name} - {self.stock} dona"
