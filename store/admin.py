from django.contrib import admin
from .models import CartItem, Catagory, Car, Cart, Order, OrderItem

# Register your models here.


@admin.register(Catagory)
class CatagoryAdmin(admin.ModelAdmin):
    '''Admin View for Catagory'''

    list_display = ('id', 'title')
    list_per_page = 10


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    '''Admin View for Car'''

    list_display = ('id', 'title', 'description',
                    'price', 'image', 'user')
    list_per_page = 10


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    '''Admin View for Cart'''

    list_display = ('id', 'created_at')
    list_per_page = 10


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    '''Admin View for CartItem'''

    list_display = ('id', 'cart', 'car', 'quantity')
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Admin View for Order'''

    list_display = ('id', 'user', 'placed_at', 'payment_status', )
    list_per_page = 10


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    '''Admin View for OrderItem'''

    list_display = ('id', 'order', 'car', 'quantity', 'price', )
    list_per_page = 10
