from django.urls import path
from .views import RegisterPage,LoginPage,LogoutView,AddressView,load_districs,AccountView,ProfileView,EditAddressView

urlpatterns = [
        path('register/',RegisterPage.as_view(),name='register'),
        path('login/',LoginPage.as_view(),name='login'),
        path('logout/',LogoutView.as_view(),name='logout'),
        path('address/',AddressView.as_view(),name='address'),    
        path('load_districts/',load_districs,name='load_districts'),
        path('account/',AccountView.as_view(),name='account'),
        path('profile/',ProfileView.as_view(),name='profile'),
        path('update_address/',EditAddressView.as_view(),name='update_address')
]