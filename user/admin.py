from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profil

# Register your models here.
def make_published(modeladmin, request, queryset):
    #print(request.POST.getlist(admin.ACTION_CHECKBOX_NAME)[0])
    for i in request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
    	profil=Profil.objects.get(id=i)
    	if profil.user != None:
    		User.objects.get(id=int(profil.user.id)).delete()
    	

make_published.short_description = "Supprimer les profils sélectionnés"
class ProfilAdmin(admin.ModelAdmin):
	
	actions = [make_published]
	class Meta:
		model = Profil

admin.site.register(Profil,ProfilAdmin)
