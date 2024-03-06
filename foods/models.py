from collections.abc import Iterable
from django.db import models
from django.template.defaultfilters import slugify

from django.utils.safestring import mark_safe

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=155, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    category_disc = models.TextField()
    icon_str = models.ImageField(default='hello.png', upload_to='categories/')

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        return super(Category, self).save(*args, **kwargs)

class Item(models.Model):
    item_name = models.CharField(max_length=155, unique=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    item_disc = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2, default=9.99)
    item_img = models.ImageField(default='item.jpg', upload_to='items/')
    
    def __str__(self):
        return self.item_name
    
    def admin_image(self):
        return mark_safe('<img src="{}" width="50">'.format(self.item_img.url))
    admin_image.short_description = 'Image'
    admin_image.allow_tags = True
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.item_name)
        return super(Item, self).save(*args, **kwargs)
    

