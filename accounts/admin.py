from django.contrib import admin
from .models import District,State,ContactAddress,User
from django.contrib.auth.models import Group

class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_state_name']

    def get_state_name(self, obj):
        
        return obj.state.name or 'No State'
    
    get_state_name.short_description = 'State'

# Register your models here.
admin.site.register(District, DistrictAdmin)
admin.site.register(State)
admin.site.unregister(Group)

