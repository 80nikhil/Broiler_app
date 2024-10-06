from django.contrib import admin
from . models import * 

admin.site.register(user)
class ctype_data_Admin(admin.ModelAdmin):
    model = ctype_data
    search_fields = ['id','title','abbreviation','alias_name']
    list_display = ['id','title','abbreviation','alias_name']
admin.site.register(ctype_data,ctype_data_Admin)
class broiler_region_Admin(admin.ModelAdmin):
    model = broiler_region
    search_fields = ['id','regionid','region','abbreviation','alias_name']
    list_display = ['id','regionid','region','abbreviation','alias_name']
admin.site.register(broiler_region,broiler_region_Admin)