from django.contrib import admin
from .models import Hairsalon, HairsalonService

class HairsalonServiceAdmin(admin.ModelAdmin):
    list_display = ('salon_HName', 'menu_name', 'service_name', 'price')
    list_filter = ('salon__HName', 'menu_name')  

    def salon_HName(self, obj):
        return obj.salon.HName
    
    salon_HName.short_description = 'Hairsalon Name' 

admin.site.register(Hairsalon)
admin.site.register(HairsalonService, HairsalonServiceAdmin)
