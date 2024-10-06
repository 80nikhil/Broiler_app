from django.contrib import admin
from . models import * 

admin.site.register(user)
class ctype_data_Admin(admin.ModelAdmin):
    model = ctype_data
    list_display = ['id','title','abbreviation','alias_name']
    def get_question(self, obj):
        return obj.question.question
admin.site.register(ctype_data,ctype_data_Admin)
class broiler_region_Admin(admin.ModelAdmin):
    model = broiler_region
    list_display = ['id','regionid','region','abbreviation','alias_name']
    def get_question(self, obj):
        return obj.question.question
admin.site.register(broiler_region,broiler_region_Admin)