from django.db import models
from accounts.models import User

import uuid
from foods.models import Item
from accounts.models import ContactAddress


# Create your models here.
class Cart(models.Model):

    user = models.ForeignKey(User,related_name='cart', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    
    
    def cart_price(self):
        total = 0
        cart_items = self.cart_items.all()
        for i in cart_items:
            total = total + float(i.item_total_price())
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.item.item_name} - {self.quantity}'
    
    def item_total_price(self):
        return self.item.price * self.quantity
    
class ShippingAddress(models.Model):
    house_number = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    pin = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

class Order(models.Model):

    STATUS_CHOICES = (
        ('processing','Processing'),
        ('delivered','Delivered'),
        ('cancelled','Cancelled'),
        
    )

    cart = models.OneToOneField(Cart, on_delete=models.CASCADE,)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(default=9.99,max_digits=26, decimal_places=2)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    invoice  = models.UUIDField(unique=True, default=uuid.uuid4)
    status = models.CharField(choices = STATUS_CHOICES, default='processing', max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' - ' + str(self.invoice) + ' - ' + self.status
    
    def get_address(self):
        return self.shipping_address.objects.get(user=self.user)
