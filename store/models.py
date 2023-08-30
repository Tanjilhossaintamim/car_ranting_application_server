from uuid import uuid4
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
# Create your models here.


class Catagory(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Car(models.Model):
    title = models.CharField(max_length=255)

    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='car', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)
    catagory = models.ForeignKey(Catagory, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])


class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLEATE = 'C'
    PAYMENT_FAILED = 'F'
    PAYMENT_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLEATE, 'Compleate'),
        (PAYMENT_FAILED, 'Failed'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)
    placed_at = models.DateField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_CHOICES, default=PAYMENT_PENDING)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    car = models.ForeignKey(Car, on_delete=models.CASCADE,
                            related_name='orderitems')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
