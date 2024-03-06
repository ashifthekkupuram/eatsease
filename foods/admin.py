from django.contrib import admin
from .models import Category, Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ['admin_image','item_name','get_cat','price']
    exclude = ['slug']

    def get_cat(self, obj):
        return obj.category.category_name
    
    get_cat.short_description = 'Category'

class CategoryAdmin(admin.ModelAdmin):
    exclude = ['slug']

    


# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
