
from django.urls import path,include
from django.conf.urls import url
from . import views
app_name= 'user'

urlpatterns = [
    path('',views.base),
    url(r'^login/(?P<id>[0-9]+)/$',views.login, name='login'),
    path('logout',views.logout),
    url(r'^signup/(?P<id>[0-9]+)/$',views.signup,name='signup'),
]
