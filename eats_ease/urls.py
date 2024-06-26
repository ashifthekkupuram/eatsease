from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'EatsEase Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('foods.urls')),
    path('auth/',include('accounts.urls')),
    path('cart/',include('carts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
                          
