from django.contrib import admin
from .models import Cart,CartItem,Order,ShippingAddress
from accounts.models import ContactAddress

from django.utils.html import format_html
from django.urls import reverse

from django.contrib import admin

class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'status', 'created', 'get_cart_items', 'get_shipping_address']
    readonly_fields = ['user', 'price', 'invoice', 'created', 'get_cart_items', 'get_shipping_address']
    ordering = ['-status',]
    exclude = ['cart','shipping_address']

    def has_add_permission(self, request):
        return False  # Disable the ability to add new orders from the admin

    def get_cart_items(self, obj):
        try:
            cart_items = obj.cart.cart_items.all()
            return ''.join([f"{item.item.item_name} - {item.quantity} - ₹{item.item_total_price()}\n" for item in cart_items])
        except AttributeError:
            return "N/A"
    get_cart_items.short_description = 'Items'

    def get_shipping_address(self, obj):
        try:
            address = obj.shipping_address
            return f"{address.house_number}, {address.street}, {address.city}, {address.district}, {address.state}, {address.pin}, {address.phone}"
        except AttributeError:
            return "N/A"
    get_shipping_address.short_description = 'Shipping Address'

admin.site.register(Order, OrderAdmin)








