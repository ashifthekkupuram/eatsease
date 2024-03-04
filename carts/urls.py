from django.urls import path
from .views import CartView,RemoveCartItem,OrderView

urlpatterns = [
    path('page/', CartView.as_view(), name='cart'),
    path('remove/<int:pk>', RemoveCartItem.as_view(), name='remove_item'),
    path('order/<int:pk>', OrderView.as_view(), name='order'),
]