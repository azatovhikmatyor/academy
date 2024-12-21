from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from inventory.models import Product


class Order(models.Model):
    salesman = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total = models.PositiveBigIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_actual = models.PositiveBigIntegerField()
    price_sold = models.PositiveBigIntegerField()
    quantity = models.FloatField()
    total = models.PositiveBigIntegerField()
    order_date = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'