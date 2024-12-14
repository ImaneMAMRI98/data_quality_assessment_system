
from django.contrib import admin
# Register your models here.
from .models import Int,Float,String,MetaData,Services,Date,semantic_rules
from django.shortcuts import  get_object_or_404
admin.site.disable_action('delete_selected')



admin.site.register(Int)
admin.site.register(Float)
admin.site.register(String)
admin.site.register(MetaData)
admin.site.register(Services)
admin.site.register(Date)
admin.site.register(semantic_rules)
