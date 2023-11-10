from django.contrib import admin
from .models import Hairsalon, HairsalonService

#미용실
class HairsalonAdmin(admin.ModelAdmin):
    list_display = ('HID', 'HName', 'HLoc', 'HRegion')
    list_filter = ('HRegion',)
    
admin.site.register(Hairsalon, HairsalonAdmin)

#서비스
class HairsalonServiceAdmin(admin.ModelAdmin):
    list_display = ('salon_HName', 'menu_name', 'service_name', 'price')
    list_filter = ('salon__HName', 'menu_name')  

    def salon_HName(self, obj):
        return obj.salon.HName
    
    salon_HName.short_description = 'Hairsalon Name' 

admin.site.register(HairsalonService, HairsalonServiceAdmin)
