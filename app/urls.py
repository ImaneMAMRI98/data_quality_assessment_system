from django.urls import path,include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
app_name= 'app'

urlpatterns = [
   
    #lister les categories
    url(r'^parametrage/',views.parametrage,name='parametrage'),
    url(r'^choix_type/',views.choix_type,name='choix_type'),
    url(r'^param2/',views.param2,name='param2'),
    url(r'^param3/',views.param3,name='param3'),
    url(r'^param4/',views.param4,name='param4'),
    url(r'^catalog/',views.catalog,name='catalog'),
    url(r'^catalog2/',views.catalog2,name='catalog2'),
    url(r'^multimedia/',views.multimedia,name='multimedia'),
    url(r'^evalMul/',views.evalMul,name='evalMul'),
    url(r'^mulamelioration/',views.mulamelioration,name='mulamelioration'),
    
    url(r'^downloadCSV',views.downloadCSV,name='downloadCSV'),

    url(r'^download/',views.download,name='download'),
    url(r'^downloadmul/',views.downloadmul,name='downloadmul'),
    url(r'^downloadZIP',views.downloadZIP,name='downloadZIP'),
    url(r'^display', views.display, name ="display"),

    url(r'^amelioration/',views.amelioration,name='amelioration'),
    url(r'^dimensionss/',views.dimensionss,name='dimensionss'),
    #/id/categery/
    
    
    url(r'^evaluer/$',views.evaluer, name ='evaluer'),
   
    
]
