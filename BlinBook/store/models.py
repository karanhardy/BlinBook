from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to="products/",null = True, blank = True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Order(models.Model):
    Payment_Choices = [
        ('COD', 'Cash on Delivery'),
        ('Online', 'Online Payment'),
        ('UPI', 'UPI'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=Payment_Choices, default='COD')

    def __str__(self):
        return f"Order {self.product.name} by {self.user.username} using {self.payment_method}"

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity} for {self.user.username}"