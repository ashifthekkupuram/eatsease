from django.urls import path
from .views import (HomeView,FoodDetailView,OrderListView, FavView,AddToFav,OrderDetail)

urlpatterns = [
    path('', HomeView.as_view(),name='home'),
    path('order_list/', OrderListView.as_view(),name='order_list'),
    path('favourites/',FavView.as_view(),name='fav'),
    path('order_detail/<str:invoice>',OrderDetail.as_view(),name='order_detail'),
    path('add_to_fav/<str:slug>/',AddToFav.as_view(),name='fav_add'),
    path('<str:slug>/', FoodDetailView.as_view(),name='food'),
]