from django.conf import settings
from django.contrib import admin
from django.db import models
from uuid import uuid4
"""
models.py
This module contains the Django models for an e-commerce application. The models represent the core entities of the application, including promotions, collections, products, customers, orders, addresses, carts, and cart items.
Classes:
    - Promotion: Represents a promotional offer with a description and discount.
    - Collection: Represents a collection of products, with a title and a featured product.
    - Product: Represents a product with attributes such as title, slug, description, unit price, inventory, last updates, collection, and promotions.
    - Customer: Represents a customer with personal details and membership status.
    - Order: Represents an order placed by a customer, including payment status and associated customer.
    - OrderItem: Represents an item in an order, including the product and quantity.
    - Address: Represents a customer's address with street, city, zip code, and associated customer.
    - Cart: Represents a shopping cart with a creation timestamp.
    - CartItem: Represents an item in a cart, including the product and quantity.
References:
    - Django Documentation: https://docs.djangoproject.com/en/stable/topics/db/models/
    - Django Validators: https://docs.djangoproject.com/en/stable/ref/validators/
    - Django Model Field Reference: https://docs.djangoproject.com/en/stable/ref/models/fields/
"""
from django.core.validators import MinValueValidator

# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255) 
    featured_product = models.ForeignKey(
        'Product', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='+'
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
    

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(1)]
        )
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    
    MEMBERSHIP_CHOICE = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    # first_name = models.CharField(max_length=150)
    # last_name = models.CharField(max_length=150)
    # email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICE, default= MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)
    
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETED = 'C'
    PAYMENT_FAILED = 'F'
    
    PAYMENT_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETED, 'Complete'),
        (PAYMENT_FAILED, 'Failed')
    ]
    
    payment_status = models.CharField(max_length=1 ,choices=PAYMENT_CHOICES, default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)    
    city = models.CharField(max_length=255)    
    zip = models.IntegerField(null=True)
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    
    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)