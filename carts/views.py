from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cart,CartItem,Order,ShippingAddress


# Create your views here.
class CartView(LoginRequiredMixin, View):
    def get(self, request):

        cart = Cart.objects.get_or_create(completed=False, user=request.user)
        cart_items = cart[0].cart_items.all()
        return render(request, 'carts/cart.html', {
            'cart':cart[0],
            'cart_items':cart_items,
        })
    
class RemoveCartItem(LoginRequiredMixin, View):
    def get(self, request, pk):
        url = request.META.get('HTTP_REFERER')
        cart_item = CartItem.objects.get(pk=pk)
        cart_item.delete()

        return redirect(url)
    
class OrderView(LoginRequiredMixin, View):
    def get(self, request, pk):
        cart = Cart.objects.get(id=pk)
        cart.completed = True
        cart.save()
        ship = ShippingAddress.objects.create(
            house_number = request.user.user_address.house_number or None,
            street = request.user.user_address.street,
            city =  request.user.user_address.city ,
            state = request.user.user_address.state.name,
            district = request.user.user_address.district.name,
            pin = request.user.user_address.pin,
            phone = request.user.user_address.phone.as_e164,
        )
        ship.save()
        order = Order.objects.create(
            cart = cart,
            user = request.user,
            shipping_address = ship,
            price = float(cart.cart_price())
        )
        order.save()
        return render(request, 'carts/order.html', {'order':order})

