from django.db import models
from django.contrib.auth.models import AbstractUser

from foods.models import Item


from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    profile = models.ImageField(default='profile.jpg', upload_to='profiles/')
    favs = models.ManyToManyField(Item, related_name='favs', blank=True, symmetrical=False)
    # address = models.TextField(null=True)
    # phone = PhoneNumberField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def check_address(self):
        try:
            return self.user_address
        except:
            return None
        
    
    def cart_items_count(self):
        from django.apps import apps

        Cart = apps.get_model('carts', 'Cart')
        try:
            # Assuming 'cart' is a RelatedManager, use .filter() to filter carts
            incomplete_carts = self.cart.filter(completed=False)
            cart_items_count = sum(cart.cart_items.all().count() for cart in incomplete_carts)
        except Cart.DoesNotExist:
            cart_items_count = 0

        return cart_items_count

    
class State(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name        
    
class ContactAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='user_address', null=True, blank=True)
    house_number = models.CharField(max_length=255, null=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    pin = models.CharField(max_length=6)
    phone = PhoneNumberField(region="IN")
        
    