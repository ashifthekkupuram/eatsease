from django.shortcuts import render,redirect
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from .models import Item,Category
from carts.models import Cart, CartItem, Order

from django.template import RequestContext

# Create your views here.
class HomeView(LoginRequiredMixin, View):
    def get(self, request):

        cat = request.GET.get('cat',None)

        if cat is not None:
            cat_obj = Category.objects.get(slug=cat)
            items = Item.objects.filter(category=cat_obj)
        else:
            items = Item.objects.all()    

        categories = Category.objects.all()

        context = {
            'items':items,
            'categories': categories
        }

        return render(request, 'foods/home.html', context,)
    
class FoodDetailView(LoginRequiredMixin, View):
    def get(self, request, slug):
        try:
            item = Item.objects.get(slug=slug)
        except:
            item = ''    
        return render(request, 'foods/food_detail.html', context={
            'item':item
        })

    def post(self, request, slug):
        url = request.META.get('HTTP_REFERER')
        cart = Cart.objects.get_or_create(completed=False, user=request.user)
        item = Item.objects.get(slug=slug)
        quantity = request.POST.get('quantity')
        cart_item, created = CartItem.objects.get_or_create(cart=cart[0],item=item)
        if created:
            cart_item.quantity = quantity
            cart_item.save()
            return redirect(url)
        else:
            cart_item.quantity = int(cart_item.quantity) + int(quantity)
            cart_item.save()
            return redirect(url)
        
class OrderListView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created')
        return render(request, 'foods/order_list.html', {'orders':orders})

class FavView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        favs = user.favs.all()
        return render(request,'foods/fav.html',{'favs':favs})

class AddToFav(LoginRequiredMixin, View):
    def get(self, request, slug):
        url = request.META.get('HTTP_REFERER')
        item = Item.objects.get(slug=slug)
        user = request.user
        if item in user.favs.all():
            user.favs.remove(item)
        else:
            user.favs.add(item)
        return redirect(url)

class OrderDetail(LoginRequiredMixin, View):
    def get(self, request, invoice):
        order = Order.objects.get(invoice=invoice)
        return render(request, 'foods/order_detail.html',{'order':order})
    
    def test_func(self):
        pass
